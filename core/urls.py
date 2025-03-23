from django.urls import path
from .views import HomeView, UserLoginView, user_signup, MainPage, user_logout

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="user_login"),
    path('logout/', user_logout, name="user_logout"),
    path('signup/', user_signup, name="user_signup"),
    path('home/', HomeView.as_view(), name='home'),
    path('', MainPage.as_view(), name="main_page"),
]
