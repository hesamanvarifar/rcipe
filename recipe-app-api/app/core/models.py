import email
from re import T

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email :
            raise ValueError('Email must be provide')

        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,  password):
        if not email :
            raise ValueError('Email must be provide')

        superuser = self.model(
            email = self.normalize_email(email)
        )
        
        superuser.set_password(password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.save()
        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model """

    """
        email: (username) , 
        name  , is_active  , is_staff 
    """

    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active =models.BooleanField(default=True)
    is_staff =models.BooleanField(default=False)

    objects =UserManager()
    USERNAME_FIELD = "email"

    


class Tag(models.Model):
    """
        Fields: name , user

    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
        Fields: name , user
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    """
        Fields: user , title , time_miniutes , price, link , ingredients , tags
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_miniutes = models.IntegerField()
    price = models.IntegerField()
    link = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
