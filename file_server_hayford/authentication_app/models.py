from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class SignUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class signUser(AbstractUser):
    username = models.CharField(max_length = 200, unique=True)
    email = models.EmailField(unique=True)
    
    # firstname = models.CharField(max_length = 200)
    # lastname = models.CharField(max_length = 200)
    # confirmPassword = models.CharField(max_length=200, unique=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = SignUserManager()