from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import UserSignUpForm
from django.contrib import messages
from django.contrib.auth import login, authenticate


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
