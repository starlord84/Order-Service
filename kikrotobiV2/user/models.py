from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, username, contact_phone, password, **extra_fields):
        if contact_phone is None:
            raise TypeError("Users should have contact phone")
        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        return user

    def create_superuser(self, password, contact_phone, username, **extra_fields):
        if password is None:
            raise TypeError("Password should not be none")
        user = self.create_user(username, contact_phone, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    organization = models.ForeignKey(
        'order.Organization', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='organization'
    )
    contact_phone = models.CharField(max_length=15, unique=True, db_index=True)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    is_staff = models.BooleanField(default=False, help_text="Сотрудник")
    is_superuser = models.BooleanField(default=False, help_text="админ")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "contact_phone",
    ]
    objects = UserManager()

    def __str__(self):
        return self.username
