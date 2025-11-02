from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from SchoolDiary.decorators import anonymous_required


# Create your views here.
class RegisterView(View):
    @staticmethod
    @anonymous_required
    def get(request):
        return render(request, 'common/register.html')

    @staticmethod
    @anonymous_required
    def post(request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if User.objects.filter(username=username).exists():
            return render(request, 'common/register.html', {'error': 'Username already registered'})

        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        new_user.save()
        return redirect('login')


class LoginView(View):
    @staticmethod
    @anonymous_required
    def get(request):
        return render(request, 'common/login.html')

    @staticmethod
    @anonymous_required
    def post(request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'common/login.html', {'error': 'Invalid username or password'})


class ProfileView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return render(request, 'common/profile.html', {'user': request.user})
        else:
            return redirect('login')


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('login')