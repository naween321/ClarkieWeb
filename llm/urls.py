from django.urls import path
from .views import get_answer

urlpatterns = [
    path('get-answer/', get_answer, name='get-answer'),
]
