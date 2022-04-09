
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):

    ''' Models' settings. '''
    # Remove some columns that we don't need.
    first_name = None
    last_name = None

    # Customize some existed columns.
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=50)

    # Add our columns.
    name = models.CharField(max_length=15, null=True, blank=True, default='新使用者')
    phone = models.CharField(max_length=10, null=True, blank=True)

    # Set REQUIRED_FIELDS.
    REQUIRED_FIELDS = []

    # Replace the USER_NAME_FIELD.
    USER_NAME_FIELD = 'username'

    # Set objects.
    objects = UserManager()

class Closet(models.Model):

    ''' Models' settings. '''
    # Self settings.
    APPEARANCE_CHOICES = [
        (1, 'CLOSET_APPEARANCE_1'),
        (2, 'CLOSET_APPEARANCE_2')
    ]

    name = models.CharField(max_length=15, default='我的衣櫃', null=True, blank=True)
    apearance = models.IntegerField(choices=APPEARANCE_CHOICES, default=0)

    # Foreign key setting.
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    clothes = models.ManyToManyField('Clothe')
    outfits = models.ManyToManyField('Outfit')


class Clothe(models.Model):

    ''' Models' settings. '''
    # Choices
    FORMAL_CHOICES = [
        (True, '正式'),
        (False, '非正式')
    ]

    WARMNESS_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3')
    ]

    # Self settings.
    name = models.CharField(max_length=50)
    image = models.ImageField()
    isFormal = models.BooleanField(choices=FORMAL_CHOICES)
    warmness = models.IntegerField(choices=WARMNESS_CHOICES)

    # Foreign keys.
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    style = models.ManyToManyField('Style')
    shoeStyle = models.ManyToManyField('ShoeStyle')
    color= models.ManyToManyField('Color')


class Outfit(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)
    image = models.ImageField()
    date = models.DateField()

    # Foreign key.
    clothes = models.ManyToManyField('Clothe')


class Company(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)
    url = models.URLField()


class Type(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)


class Style(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)


class ShoeStyle(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)


class Color(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)
    hexCode = models.CharField(max_length=7)


class Wallet(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)
    balance = models.IntegerField()


class TransactionLog(models.Model):

    ''' Models' settings. '''
    datetime = models.DateTimeField()
    amount = models.IntegerField()
    log = models.CharField(max_length=100)

    # Foreign key.
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE)


