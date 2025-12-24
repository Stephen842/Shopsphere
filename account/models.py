from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django_countries.fields import CountryField
from django.utils import timezone


# Create your models here.
class UsersManager(BaseUserManager):
    """
    Custom manager for User.

    Handles:
    - create_user: standard user with email, name, username, country.
    - create_superuser: admin user with elevated permissions.
    """
    def create_user(self, email, name, username, country, password=None):
        if not email:
            raise ValueError('Enter Email address')
        if not name:
            raise ValueError('Enter Full name')
        if not username:
            raise ValueError('Enter Username')
        if not country:
            raise ValueError('Enter Country')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            username=username,
            country=country,
        )
        user.set_password(password)  # Hash the password
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, username, country, password=None):
        user = self.create_user(
            email=email,
            name=name,
            username=username,
            country=country,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True

        if user.is_staff is not True:
            raise ValueError('Superuser must have is_staff=True')
        if user.is_superuser is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):  # Add PermissionsMixin here
    """
    Custom User model for ShopSphere.

    Fields:
    - Core: name, username, email, country, date_joined.
    - Access control: is_active, is_staff, is_superuser.
    """
    name = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    country = CountryField(blank=False, blank_label='Select Country',)
    date_joined = models.DateTimeField(default=timezone.now)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username', 'country']

    def save(self, *args, **kwargs):
        """Ensure username and email are stored in lowercase"""
        self.email = self.email.lower()
        self.username = self.username.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_full_name(self):
        """Return the user's full name"""
        return self.name

    def get_short_name(self):
        """Return the short name (username in this case)"""
        return self.username
    
    class Meta:
        verbose_name_plural = 'My User'