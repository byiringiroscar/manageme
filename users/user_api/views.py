from rest_framework.response import Response
from rest_framework.decorators import APIView, api_view
from users.user_api.serializers import RegisterUserSerializer, ClientMessageSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework import views, response, permissions, authentication, filters, generics, status
from rest_framework.authtoken.models import Token
from users.user_api.serializers import UserSerializer
from rest_framework import status

User = get_user_model()


class CreateUserAPIView(generics.CreateAPIView):  # register user by create
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def perform_create(self, serializer):
        data = {}

        user = serializer.save()
        token = Token.objects.get(user=user).key

        data['token'] = token


@api_view(['POST', ])
def register_user_view(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "succesfully new created"
            data['phone'] = user.phone_number
            data['name'] = user.name
            data['user_login'] = user.user_login
            token = Token.objects.get(user=user)
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

@api_view(['POST', ])
def send_message(request):
    if request.method == 'POST':
        serializer = ClientMessageSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['respnse'] = "Message sent succesfully"
            data['email'] = user.email
            data['subject'] = user.subject
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)




