from django.db import models
import uuid
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Name is requried !!")
        if not password:
            raise ValueError("Password is Required !!")
        user = self.model(username = username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Name is requried !!")
        if not password:
            raise ValueError("Password is Required !!")
        user = self.create_user(username = username, password = password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    username = models.CharField(max_length = 255, unique = True)
    password = models.CharField(max_length = 255)
    is_staff = models.BooleanField(default = True)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()


class Collection(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Movie(models.Model):
    uuid = models.CharField(max_length=100, primary_key = True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    genres = models.CharField(max_length=100)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
