from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please enter a valid email address"))


    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        email = self.normalize_email(email) # It normalizes the email address (lowercases the domain part of the email) to ensure consistency and avoid case-related issues when working with emails.
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields) # It uses self.model (which is the user model associated with the manager) to create a new user object.
        if password:
            user.set_password(password) # This method internally handles password hashing for security purposes.
        user.save(using=self._db) # The using=self._db argument specifies the database to use for saving the user. This allows for flexibility in multi-database setups.
        return user
    
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, first_name, last_name, password, **extra_fields)



# Here are some examples of custom methods you might consider adding to your UserManager:
# - Custom User Query Methods:
 # -- get_users_by_category, get_active_users, get_user_by_id, filter_users_by_criteria, search_users, get_users_created_between
# - User Management and Updates:
 # -- update_user_profile, toggle_user_status
# - Password Management:
 # -- change_password, reset_password
# - User Deletion or Archiving:
 # -- soft_delete_user, delete_inactive_users