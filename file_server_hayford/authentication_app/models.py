from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class SignUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not password:
            raise ValueError('Password is Required')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        

    def create_superuser(self, email, password=None, **extra_fields):
        try:
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            return self.create_user(email, password, **extra_fields)
        except:
            raise ValueError('An Error Occured Please Try Again')

class signUser(AbstractUser):
    username = models.CharField(max_length = 200, unique=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = SignUserManager()