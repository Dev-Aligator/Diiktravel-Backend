from django.urls import path
from . import views

urlpatterns = [
    path('get/places/', views.getPlaceData),
    # path('get/skills/', views.getSkillsData),
    # path('get/projects/', views.getProjectsData),
    # path('post/contact/', views.addContact),
]