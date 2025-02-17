from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from .models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
        },
        required=['email', 'password']
    ),
    responses={200: 'Login successful', 400: 'Bad request'}
)
@api_view(['POST'])
def login(request):
    if 'email' not in request.data or 'password' not in request.data:
        return Response({"error" : "Invalid input "}, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(CustomUser, email = request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"error" : "Invalid credentials "}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token" : token.key}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
        },
        required=['email', 'password']
    ),
    responses={200: 'Login successful', 400: 'Bad request'}
)
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = CustomUser.objects.get(email=serializer.data['email'])
        user.set_password(serializer.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token' : token.key, 'email' : serializer.data,}, status=status.HTTP_201_CREATED)
    return Response({"Error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
        },
        required=['email', 'password']
    ),
    responses={200: 'Login successful', 400: 'Invalid input or credentials'}
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(instance=request.user)
    return Response({"data" :serializer.data}, status=status.HTTP_200_OK)