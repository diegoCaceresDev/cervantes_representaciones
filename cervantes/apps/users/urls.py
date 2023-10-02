from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.users.views import register, user_login, user_logout

app_name = 'user'

urlpatterns = [
    # Logins
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('user_logout', user_logout, name='logout')
    ]