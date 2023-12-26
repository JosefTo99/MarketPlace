from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer, EmptySerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .models import OneTimePassword
from rest_framework.permissions import IsAuthenticated
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator






class RegisterUserView(GenericAPIView):
    serializer_class=UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)  # the data that serializer take is request data
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data
            # user_instance = User.objects.get(email=user['email'])
            # token = Token.objects.create(user=user_instance)
            
            send_code_to_user(user['email'])

            return Response({
                # 'token': token.key ,
                'user':user,
                'message':f'hi thanks for signing up, verify your email'
            }, 
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserRegisterSerializer(users, many=True)
        return Response({
                'data':serializer.data,
            },status=status.HTTP_200_OK)
    


class VerifyUserEmail(GenericAPIView):  #receive the Otp that was sent to the user and validate it
    serializer_class = EmptySerializer 
    def post(self, request):
        otpcode = request.data.get('otp')
        try:
            user_code_obj = OneTimePassword.objects.get(code = otpcode) # we try to get the user object from our OneTimePassword object (because they have one to one relationship)
            user = user_code_obj.user
            if not user.is_verified:  # the user not applied code before
                user.is_verified = True
                user.save()
                return Response({
                    'message' : 'account email verified successfully'
                }, status=status.HTTP_200_OK)
            
            return Response({
                'message':'code is invalid user already verified'
            }, status=status.HTTP_204_NO_CONTENT)
        
        except OneTimePassword.DoesNotExist:
            Response({'message':'passcode not provided'}, status=status.HTTP_404_NOT_FOUND)


    


class LoginUserView(GenericAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        serializer= self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    




class TestingAuthenticatedReq(GenericAPIView):
    permission_classes=[IsAuthenticated] # indicates that this view requires the user to be authenticated to access its functionality. 
                                              # IsAuthenticated is a built-in DRF permission class that ensures the user making the request is authenticated.

    # HTTP GET Request handler
    def get(self, request):

        data={
            'msg':'its works'
        }
        return Response(data, status=status.HTTP_200_OK)
    



# class LoginUserView(GenericAPIView):
#     serializer_class=UserLoginSerializer

#     def post(self, request):
#         user = get_object_or_404(User, email = request.data['email'])
#         if not user.check_password(request.data['password']):
#             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
#         token, created = Token.objects.get_or_create(user=user)
#         serializer = UserLoginSerializer(instance=user)
#         return Response({"token": token.key, "user": serializer.data})
        


# from rest_framework.decorators import api_view
# from rest_framework.decorators import authentication_classes, permission_classes
# from rest_framework.authentication import SessionAuthentication, TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     return Response("passed for {}".format(request.user['email']))