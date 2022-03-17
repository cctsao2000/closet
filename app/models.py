
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):

    ''' Models' settings. '''
    # Remove some columns that we don't need.
    first_name = None
    last_name = None

    # Customize some existed columns.
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=50, null=True, blank=True)

    # Add our columns.
    nickname = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)

    # Set REQUIRED_FIELDS.
    REQUIRED_FIELDS = []

    # Replace the USER_NAME_FIELD.
    USER_NAME_FIELD = 'username'


class Closet(models.Model):

    ''' Models' settings. '''
    # Self settings.
    AppearanceChoices = models.IntegerChoices(
        'AppearanceChoices',
        'CLOSET_APPEARANCE_1 CLOSET_APPEARANCE_2'
    )

    name = models.CharField(max_length=15, default='我的衣櫃', null=True, blank=True)
    apearance = models.IntegerField(choices=AppearanceChoices, default=0)

    # Foreign key setting.
    user = models.ForeignKey('User')


class Clothe(models.Model):

    ''' Models' settings. '''
    TYPE_CHOICES =




