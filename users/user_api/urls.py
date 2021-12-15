from users.user_api.views import RegisterUserSerializer
from users.user_api.views import CreateUserAPIView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from users.user_api.views import register_user_view
from rest_framework.authtoken.views import obtain_auth_token
name = 'users'

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'), # user registration api
    path('newregister/', register_user_view, name='regi'),
    path('login', obtain_auth_token, name='login'),



]
