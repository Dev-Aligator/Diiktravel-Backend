from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Place
from .serializers import PlaceSerializer
import random
from thefuzz import fuzz
@api_view(['GET'])
def getPlaceData(request):
    page = request.GET.get('page', 1)
    page = int(page)
    keyword = request.GET.get('keyword', 1)

    similarity_threshold = 50
    # write new code
    startIndex = 12*(page-1)
    endIndex = 12*page
    all_places = Place.objects.all()

    if keyword:
        filtered_places = [
            (place, fuzz.ratio(keyword, place.name)) for place in all_places if fuzz.ratio(keyword, place.name) >= similarity_threshold
        ]
        sorted_filtered_places = sorted(filtered_places, key=lambda x: x[1], reverse=True)
        filtered_places = [place for place, _ in sorted_filtered_places]

    else:
        filtered_places = all_places

    total_filtered_places = len(filtered_places)
    places = filtered_places[startIndex:endIndex]
    serializer = PlaceSerializer(places, many=True)
    response_data = {
        'places': serializer.data,
        'total_filtered_places': total_filtered_places
    }
    return Response(response_data)

