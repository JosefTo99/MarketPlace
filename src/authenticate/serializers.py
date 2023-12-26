from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, smart_bytes
from django.urls import reverse
from .utils import send_normal_email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode




class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)


    class Meta:
        model = User
        fields = ['id','email', 'first_name','last_name','password','password2']


    def validate(self, attrs):  # It's used to validate the data sent to the serializer before creating or updating an object
                                   # The validate method is a standard method in DRF serializers used for custom field-level validation.
                                    # It takes the attrs dictionary as an argument, which contains the data to be validated.
        password = attrs.get('password','')
        password2 = attrs.get('password2','')
        email = attrs.get('email','')
        if password != password2:
            raise serializers.ValidationError("passwords do not match")
        return attrs
        
    
    def create(self, validated_data): # This method is responsible for creating a new user instance based on the validated data received by the serializer.
        user = User.objects.create_user(   # It uses User.objects.create_user() method, which is typically a custom manager method on the User model.
            email = validated_data['email'],
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            password = validated_data.get('password')
        )
        return user





class EmptySerializer(serializers.Serializer):
    pass





class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155, min_length=6)
    password=serializers.CharField(max_length=68, write_only=True)
    full_name=serializers.CharField(max_length=255, read_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']

    

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request=self.context.get('request')
        user = authenticate(request, email=email, password=password) # The authenticate function is commonly used to verify the credentials (email and password) provided by the user against stored user credentials in a database or some authentication backend.
        if not user:
            raise AuthenticationFailed("invalid credential try again")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")
        tokens=user.tokens()
        return {
            'email':user.email,
            'full_name':user.get_full_name,
            "access_token":str(tokens.get('access')),
            "refresh_token":str(tokens.get('refresh'))
        }
    


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
            
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():  # It checks if a user with the provided email exists in the User model 
            user= User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request=self.context.get('request')
            current_site=get_current_site(request).domain # it's particularly useful in scenarios where you might have multiple sites running off the same Django codebase but under different domains.
            relative_link =reverse('reset-password-confirm', kwargs={'uidb64':uidb64, 'token':token})
            abslink=f"http://{current_site}{relative_link}" # Constructs a password reset link containing the UIDB64 and token for the user.
            print(abslink)
            email_body=f"Hi {user.first_name} use the link below to reset your password {abslink}" # Creates an email body containing the reset link.
            data={
                'email_body':email_body, 
                'email_subject':"Reset your Password", 
                'to_email':user.email
                }
            send_normal_email(data)

        return super().validate(attrs)

    









   # DOC : 
    # The backend, upon successful authentication, generates an access token and sends it back as a response. The frontend receives and stores this access token securely.
    # This token is usually stored in memory (e.g., in a variable) or in more secure storage mechanisms like browser cookies,
                                                                                          # local storage, or secure storage available in mobile apps.