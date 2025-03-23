from django.db import models
from django.contrib.auth.models import AbstractUser


class DateTimeField(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class User(AbstractUser):
#     age = models.PositiveIntegerField(null=True, blank=True)
#     nationality = models.CharField(max_length=150)


class QuestionAnswer(DateTimeField):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person_qas')
    question = models.TextField(max_length=5000)
    answer = models.TextField(max_length=10000, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    links = models.TextField(null=True, blank=True)


