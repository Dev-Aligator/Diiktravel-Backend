from django.urls import path
from . import views

urlpatterns = [
    path('get/places/', views.PlaceAPI.as_view()),
    path('register/',views.UserRegister.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('get/user/', views.UserView.as_view()),
    path('logout/', views.UserLogout.as_view()),
    # path('get/skills/', views.getSkillsData),
    # path('get/projects/', views.getProjectsData),
    # path('post/contact/', views.addContact),
]