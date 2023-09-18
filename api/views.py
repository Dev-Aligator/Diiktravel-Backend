from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Place, UserFeature, Review, PlaceDetails
from .serializers import PlaceSerializer, UserFeatureSerializer, PlaceDetailsSerializer, ReviewSerializer
import json
from thefuzz import fuzz
import math
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

class PlaceAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        # Get query parameters
        page = int(request.query_params.get('page', 1))  # Default to 1 if 'page' is not provided
        keyword = request.query_params.get('keyword', '')
        location = request.query_params.get('location', '0.0,0.0')
        
        # Parse latitude and longitude from location string
        location_parts = location.split(',')
        user_latitude = float(location_parts[0])
        user_longitude = float(location_parts[1])
        # Calculate pagination indexes
        items_per_page = 12
        start_index = (page - 1) * items_per_page
        end_index = page * items_per_page

        places = Place.objects.all()

        # Apply keyword filtering


        filtered_places = []

        for place in places:
            # Calculate the matching score using fuzzywuzzy's fuzz.ratio function
            matching_score = 100
            if keyword:
                matching_score = fuzz.ratio(keyword, place.name)
                if matching_score < 40:
                    continue
            # Calculate the distance between the user and the place
            place_distance = getDistance(
                user_latitude,
                user_longitude,
                json.loads(place.location)['lat'],
                json.loads(place.location)['lng']
            )
            place.distance_to_user = place_distance
            
            # Calculate the place score as matching score divided by distance
            if place_distance == 0:
                place_distance = 0.000001
            place_score = ( matching_score**1.4 ) / place_distance
            # Append the place and its score to the list
            filtered_places.append((place, place_score))

        # Sort the places based on the place score in descending order
        sorted_filtered_places = sorted(filtered_places, key=lambda x: x[1], reverse=True)
        # Extract the sorted places
        sorted_places = [place for place, score in sorted_filtered_places]
        # Calculate the total filtered places
        total_filtered_places = len(sorted_places)

        # Apply ordering by distance

        # Apply pagination
        paginated_places = sorted_places[start_index:end_index]

        # Serialize the results
        serializer = PlaceSerializer(paginated_places, many=True)
        
        # Create a response dictionary
        response_data = {
            'places': serializer.data,
            'total_filtered_places': total_filtered_places,
        }
        
        return Response(response_data)


def getDistance(lat1, lng1, lat2, lng2):
    # Radius of the Earth in kilometers
    earth_radius = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lng1 = math.radians(lng1)
    lat2 = math.radians(lat2)
    lng2 = math.radians(lng2)

    # Haversine formula
    dlat = lat2 - lat1
    dlng = lng2 - lng1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = earth_radius * c

    return distance

class PlaceDetailsApi(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        placeId = request.query_params.get('placeId', '')
        if not placeId:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            placeDetails = PlaceDetails.objects.get(id=placeId)
            place = Place.objects.get(googleMapId=placeId)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        reviews = Review.objects.filter(place_id=placeId)
        serializerReview = ReviewSerializer(reviews, many=True)
        serializerDetails = PlaceDetailsSerializer(placeDetails)
        serializerPlace = PlaceSerializer(place)
        response_data = {
            'place': serializerPlace.data,
            'details' : serializerDetails.data,
            'reviews' : serializerReview.data,
        }
        return Response(response_data)

class ReviewUpdateLikes(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    def get(self, request):
        reviewId = request.query_params.get('reviewId', '')
        username = request.user.username
        review = Review.objects.get(id=reviewId)
        if not review:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        userLikedStringList = review.userLiked.split(',')
        userLikedList = [item for item in userLikedStringList if item]

        if username in userLikedList:
            review.likes -= 1
            userLikedList.remove(username)
            review.userLiked = ','.join(userLikedList)
        else:
            review.userLiked += username + ","
            review.likes += 1
        review.save()
        return Response({'likes': review.likes}, status=status.HTTP_200_OK)

        
class AddReview(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        print(request.data)
        return Response(status=status.HTTP_200_OK)




class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
	##g
    def get(self, request):
        serializer = UserSerializer(request.user)
        # userFeature = UserFeatureSerializer(user=request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class IsAuthenticated(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    def get(self, request):
        return Response({'authenticated': True}, status=status.HTTP_200_OK)