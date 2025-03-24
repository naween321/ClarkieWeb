import csv
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import UserSignUpForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from .models import QuestionAnswer
from django.conf import settings


class MainPage(TemplateView):
    template_name = 'core/main.html'


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'core/home.html'


class UserLoginView(LoginView):
    template_name = "core/login.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User Login"
        return context
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(UserLoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            print("Error")
            messages.error(request, "Invalid username or password.")
            return render(request, self.template_name)


def user_signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash the password
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect("user_login")  # Redirect to dashboard or homepage
    else:
        if request.user.is_authenticated:
            return redirect('home')
        form = UserSignUpForm()

    return render(request, "core/signup.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("main_page")


def recent_questions(request):
    questions = QuestionAnswer.objects.all().order_by('-created_at')
    response = []
    for question in questions:
        response.append({"title": question.question})
    return JsonResponse(response, safe=False)


def clark_location(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'abbrev.csv')
    query = request.GET.get('building_query')
    # List to store the CSV data
    questions = []

    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Ensure the required columns exist
            required_columns = {'id', 'link', 'title', 'excerpt', 'featured_image_url', 'coordinates'}
            if not required_columns.issubset(reader.fieldnames):
                return JsonResponse({'error': 'CSV file is missing required columns'}, status=400)

            # Iterate through each row and append to the list
            for row in reader:
                # Split coordinates into latitude and longitude
                try:
                    latitude, longitude = row['coordinates'].split(',')
                    latitude = float(latitude.strip())  # Convert to float and remove extra whitespace
                    longitude = float(longitude.strip())
                except (ValueError, IndexError):
                    return JsonResponse({'error': f"Invalid coordinates format in row with id {row['id']}"}, status=400)

                question = {
                    'id': row['id'],
                    'link': row['link'],
                    'title': row['title'],
                    'excerpt': row['excerpt'],
                    'featured_image_url': row['featured_image_url'],
                    'latitude': latitude,  # New field
                    'longitude': longitude  # New field
                }
                questions.append(question)
        if query:
            for question in questions:
                temp = str(question)
                if query in temp or query.lower() in temp or query.upper() in temp or query.title() in temp:
                    return JsonResponse(question)

        # Return the data as JSON
        return JsonResponse(questions, safe=False)  # safe=False allows a list as the root object

    except FileNotFoundError:
        return JsonResponse({'error': 'CSV file not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
