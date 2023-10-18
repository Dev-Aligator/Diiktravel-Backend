from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Place, UserFeature, Review, PlaceDetails, User, UserSavePlace, NgrokUrl
from .serializers import PlaceSerializer, UserFeatureSerializer, PlaceDetailsSerializer, ReviewSerializer, UserSavedPlaceSerializer, NgrokSerializer
import json
from thefuzz import fuzz
import math
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from .csrfDessionAuthentication import CsrfExemptSessionAuthentication, BasicAuthentication
import time
import datetime
import ast
from .app import SentimentAnalysis
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
        reviews = Review.objects.filter(place_id=placeId).order_by('-id')
        for review in reviews:
            review.relative_time_description = secondsConverter(time.time() - review.time)
        serializerReview = ReviewSerializer(reviews, many=True)
        serializerDetails = PlaceDetailsSerializer(placeDetails)
        serializerPlace = PlaceSerializer(place)
        response_data = {
            'place': serializerPlace.data,
            'details' : serializerDetails.data,
            'reviews' : serializerReview.data,
            'openingHours': getPlaceCurrentOpeningHours(placeDetails.current_opening_hours)
        }
        return Response(response_data)

class SentimentAnalysisApi(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        review = request.query_params.get('input', '')
        aspects_sentiments = SentimentAnalysis(review)
        return Response( {'aspects_sentiments' : aspects_sentiments}, status=status.HTTP_200_OK)

class NgrokAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        ngrok = NgrokUrl.objects.first()
        return Response( {'ngrok_url' : ngrok.ngrok_url}, status=status.HTTP_200_OK)

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
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        data = request.data
        try:
            userFeature = UserFeature.objects.get(user=request.user)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        try:
            Review.objects.get(author_id=request.user.id, place_id=data['placeId'])
            return Response(status=status.HTTP_409_CONFLICT)
        except:
            pass

        ## Adding 1 to place total reviews
        reviewedPlace = Place.objects.get(googleMapId=data['placeId'])
        reviewedPlace.totalRating += 1
        reviewedPlace.save()
        try:
            AuthorName = userFeature.firstName + userFeature.lastName
        except:
            AuthorName = "Default username"
        new_review = Review.objects.create(place_id=data['placeId'], author_id=request.user.id, author_name=AuthorName, rating=data['star'], relative_time_description="", time=time.time(), language="vn", original_language="vn", profile_photo_url=userFeature.photoUrl, text=data['reviewText'], translated=False )
        serializer = ReviewSerializer(new_review)
        return Response({'new_review' : serializer.data}, status=status.HTTP_200_OK)




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
        user = User.objects.get(username=request.user)
        userFeature = UserFeature.objects.get(user=user.id)
        userFeatureSerializer = UserFeatureSerializer(userFeature)
        return Response({'user': serializer.data, 'user_details' : userFeatureSerializer.data}, status=status.HTTP_200_OK)

class UpdateUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        data = request.data
        try:
            userFeature = UserFeature.objects.get(user=request.user)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        userFeature.firstName = data['firstName']
        userFeature.lastName = data['lastName']
        userFeature.photoUrl = data['photoUrl']
        userFeature.save()
        return Response(status=status.HTTP_200_OK)


class IsAuthenticated(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    def get(self, request):
        return Response({'authenticated': True}, status=status.HTTP_200_OK)


class UserSavedPlaceAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        action = request.query_params.get('action', '')
        placeId = request.query_params.get('placeId', '')
        if action == 'AddSelectedPlaceToUserSavedPlaces':
            selectedPlace = Place.objects.get(googleMapId=placeId)
            try:
                newlySavedPlace = UserSavePlace.objects.create(user=request.user, place=selectedPlace)
                serializer = UserSavedPlaceSerializer(newlySavedPlace)
                return Response({'newlySavedPlace' : serializer.data}, status=status.HTTP_200_OK)
            except Exception as error:
                print(f"An error occurred: {error}")
                return Response(status=status.HTTP_400_BAD_REQUEST)

        elif action == 'GetUserAllSavedPlaces':
            try:
                previousUserSavedPlaces = UserSavePlace.objects.filter(user=request.user)
                savedPlacesData = Place.objects.filter(usersaveplace__in=previousUserSavedPlaces)
                serializer = UserSavedPlaceSerializer(previousUserSavedPlaces, many=True)
                placesSerializer = PlaceSerializer(savedPlacesData, many=True)
                return Response({"user_saved_places" : serializer.data, "saved-places": placesSerializer.data}, status=status.HTTP_200_OK)
            except Exception as error:
                print(f"An error occurred: {error}")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif action == 'RemoveSelectedPlaceFromUserSavedPlaces':
            try:
                savedPlaceId = request.query_params.get('savedPlaceId', '')
                selectedToRemovePlace = UserSavePlace.objects.get(id=savedPlaceId)
                selectedToRemovePlace.delete()
                return Response(status=status.HTTP_200_OK)
            except Exception as error:
                print(f"An error occurred: {error}")
                return Response(status=status.HTTP_400_BAD_REQUEST)   



class UserReviewAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        action = request.query_params.get('action', '')
        if action == 'GetAllUserReviews':
            try:
                totalUserReviews = Review.objects.filter(author_id=request.user.id)
                reviewedPlacesId = [userReview.place_id for userReview in totalUserReviews]
                reviewedPlacesData = Place.objects.filter(googleMapId__in=reviewedPlacesId)
                serializer = ReviewSerializer(totalUserReviews, many=True)
                placeSerializer = PlaceSerializer(reviewedPlacesData, many=True)
                return Response({'user_total_reviews' : serializer.data, 'places_data' : placeSerializer.data}, status=status.HTTP_200_OK)
            except Exception as error:
                print(f"An error occurred: {error}")
                return Response(status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 


def secondsConverter(seconds: int):
    while True:
        if seconds < 60:
            return f"{int(seconds)}s"
        else:
            seconds //= 60
            if seconds < 60:
                return f"{int(seconds)}m"
            else:
                seconds //= 60
                if seconds < 24:
                    return f"{int(seconds)}h"
                else:
                    seconds //= 24
                    if seconds < 30:
                        return f"{int(seconds)}d"
                    else:
                        seconds //= 30
                        if seconds < 12:
                            return f"{int(seconds)} months ago"
                        return f"{int(seconds // 12)} years ago"


def getPlaceCurrentOpeningHours(current_opening_hours):
    if not current_opening_hours:
        return "Unknown opening hours"
    weeklyHours = ast.literal_eval(current_opening_hours)
    # Get the current UTC time
    utc_time = datetime.datetime.utcnow()

    # Calculate the GMT+7 offset (7 hours ahead of GMT)
    gmt7_offset = datetime.timedelta(hours=7)

    # Calculate the GMT+7 time by adding the offset to the UTC time
    gmt7_time = utc_time + gmt7_offset

    # Get the current weekday (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
    weekday = gmt7_time.weekday()

    # Get the current hour
    hour = gmt7_time.hour

    # Print the current weekday and hour in GMT+7
    # print("Current Weekday in GMT+7:", weekday)
    # print("Current Hour in GMT+7:", hour)
    return weeklyHours[weekday]
