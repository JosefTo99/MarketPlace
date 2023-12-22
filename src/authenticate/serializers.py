from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)


    class Meta:
        model = User
        fields = ['email', 'first_name','last_name','password','password2']


    def validate(self, attrs):  # It's used to validate the data sent to the serializer before creating or updating an object
                                   # The validate method is a standard method in DRF serializers used for custom field-level validation.
                                    # It takes the attrs dictionary as an argument, which contains the data to be validated.
        password = attrs.get('password','')
        password2 = attrs.get('password2','')
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



# from rest_framework import serializers
# from django.contrib.auth.models import User
# from rest_framework.validators import UniqueValidator
# from django.contrib.auth.password_validation import validate_password


# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#             required=True,
#             validators=[UniqueValidator(queryset=User.objects.all())]
#             )

#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     repeat = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'repeat', 'email')
        

#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#         )

        
#         user.set_password(validated_data['password'])
#         user.save()

#         return user


# # you might create serializer classes that define how your Django models should be serialized into JSON for an API endpoint 
# ##  or how incoming JSON data should be deserialized into Django model instances.
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from rest_framework.authtoken.views import Token




# class UserSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = User
#     fields = ['id', 'username','email','password']

#   def create(self, validated_data):
#     user = User.objects.create_user(**validated_data)
#     # Token.objects.create(user=user)
#     return user