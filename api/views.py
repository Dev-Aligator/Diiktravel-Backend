from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Place
from .serializers import PlaceSerializer
import random
@api_view(['GET'])
def getPlaceData(request):
    page = request.GET.get('page', 1)
    page = int(page)
    startIndex = 12*(page-1)
    endIndex = 12*page
    places = Place.objects.all()[startIndex:endIndex]
    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# def getSkillsData(request):
#     skills = Skill.objects.all()
#     serializer = SkillSerializer(skills, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getProjectsData(request):
#     projects = Project.objects.all()
#     serializer = ProjectSerializer(projects, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def addContact(request):
#     serializer = ContactSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     print(serializer.data)
#     print(serializer.errors)
#     return Response(serializer.data)