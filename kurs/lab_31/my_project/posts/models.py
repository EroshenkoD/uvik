from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManage(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, is_staff=False, is_superuser=False):
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not email:
            raise ValueError("User must have a email")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(first_name=first_name,
                                last_name=last_name,
                                email=email,
                                password=password,
                                is_staff=True,
                                is_superuser=True)
        user.save()
        return user


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225, unique=True)
    username = None
    access_token = None

    objects = CustomUserManage()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Posts(models.Model):
    writer = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    body = models.TextField()
    likes = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title
