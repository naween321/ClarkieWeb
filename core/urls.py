from django.urls import path
from .views import HomeView, UserLoginView, user_signup, MainPage

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="user_login"),
    path('signup/', user_signup, name="user_signup"),
    path('home/', HomeView.as_view(), name='home'),
    path('', MainPage.as_view(), name="main_page"),
]
