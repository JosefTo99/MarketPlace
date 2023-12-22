from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import User



class RegisterUserView(GenericAPIView):
    serializer_class=UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data
            
            send_code_to_user(user['email'])

            print(user)
            return Response({
                'data':user,
                'message':f'hi thanks for signing up'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserRegisterSerializer(users, many=True)
        return Response({
                'data':serializer.data,
            },status=status.HTTP_200_OK)


# from django.contrib.auth.models import User
# from .serializers import RegisterSerializer
# from rest_framework import generics


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer



# from django.shortcuts import render
# from rest_framework import viewsets
# from .serializers import  UserSerializer
# from django.contrib.auth.models import User

# # Create your views here.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer