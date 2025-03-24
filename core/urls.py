from django.urls import path
from .views import HomeView, UserLoginView, user_signup, MainPage, user_logout, \
    recent_questions

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="user_login"),
    path('logout/', user_logout, name="user_logout"),
    path('signup/', user_signup, name="user_signup"),
    path('home/', HomeView.as_view(), name='home'),
    path('recent-questions/', recent_questions, name='recent_questions'),
    path('', MainPage.as_view(), name="main_page"),
]
