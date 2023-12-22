from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email" # Specifies the field used as the unique identifier for authentication purposes. In this case, it's set to 'email', indicating that email addresses will be used for authentication instead of the default username.

    REQUIRED_FIELDS = ["first_name","last_name"]  #  Specifies a list of fields required when creating a new user via the create_user management command or other means.
 
 # This adheres to the principle of separation of concerns,
    # By separating the logic for user creation, validation, or manipulation into a separate class, it's easier for other developers 
    objects = UserManager()  # The UserManager allows you to define custom methods for creating users (create_user and create_superuser). This is beneficial when you need specific business logic or additional fields during user creation.

    def __str__(self):
        return self.email
    
    @property  # This decorator is used to define a method that can be accessed like an attribute rather than a method call. It allows you to define a method that behaves like a read-only attribute.
    def get_full_name(self):  # When accessed (user.get_full_name), it returns the concatenation of the first_name and last_name attributes of the user instance.
        return f"{self.first_name} {self.last_name}"   
    
    def tokens(self):
        pass


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.user.first_name}-passcode"
    




























