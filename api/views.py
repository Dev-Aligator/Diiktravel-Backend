from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Place
from .serializers import PlaceSerializer
import json
from thefuzz import fuzz
import math
@api_view(['GET'])
def getPlaceData(request):
    # Get query parameters
    page = int(request.GET.get('page', 1))
    keyword = request.GET.get('keyword', '')
    location = request.GET.get('location', '0.0,0.0')
    
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