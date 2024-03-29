from django.urls import path
from . import views

urlpatterns = [
    path('get/places/', views.PlaceAPI.as_view()),
    path('register/',views.UserRegister.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('get/user/', views.UserView.as_view()),
    path('logout/', views.UserLogout.as_view()),
    path('authenticate/',views.IsAuthenticated.as_view()),
    path('get/place_details/', views.PlaceDetailsApi.as_view()),
    path('post/update_review_likes/', views.ReviewUpdateLikes.as_view()),
    path('post/add_review/', views.AddReview.as_view()),
    path('post/update_user/', views.UpdateUser.as_view()),
    path('get/save_place/', views.UserSavedPlaceAPI.as_view()),
    path('get/reviews/', views.UserReviewAPI.as_view()),
    path('get/sentiment_analysis/', views.SentimentAnalysisApi.as_view()),
    path('get/ngrok_url/', views.NgrokAPI.as_view()),
    # path('get/skills/', views.getSkillsData),
    # path('get/projects/', views.getProjectsData),
    # path('post/contact/', views.addContact),
]