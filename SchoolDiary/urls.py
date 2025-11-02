from django.contrib import admin
from django.urls import path, include

from common.views import LoginView, RegisterView, LogoutView, ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('teacher/', include('teacher.urls'), name='teacher'),
    path('student/', include('student.urls'), name='student'),
]
