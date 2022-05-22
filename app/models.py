
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
    nickname = models.CharField(max_length=15, null=True, blank=True, default='新使用者')

    phone = models.CharField(max_length=10, null=True, blank=True)

    # Set REQUIRED_FIELDS.
    REQUIRED_FIELDS = []

    # Replace the USER_NAME_FIELD.
    USER_NAME_FIELD = 'username'

    # Set objects.
    objects = UserManager()

    # Foreign key.
    friends = models.ManyToManyField('User')

    USERNAME_FIELD = 'username'


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
    clothes = models.ManyToManyField('Clothe', blank=True)
    outfits = models.ManyToManyField('Outfit', blank=True)


class Clothe(models.Model):

    ''' Models' settings. '''
    # Choices
    FORMAL_CHOICES = [
        (True, '正式'),
        (False, '休閒')
    ]

    WARMNESS_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    # Self settings.
    name = models.CharField(max_length=50, default='', blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    isFormal = models.BooleanField(choices=FORMAL_CHOICES, default=False, blank=True, null=True)
    warmness = models.IntegerField(choices=WARMNESS_CHOICES, default=3, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    # Foreign keys.
    company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE, blank=True, null=True)
    style = models.ManyToManyField('Style', blank=True, null=True)
    shoeStyle = models.ManyToManyField('ShoeStyle', blank=True, null=True)
    color= models.ManyToManyField('Color', blank=True, null=True)


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

    def __str__(self):
        return self.name


class Type(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Style(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ShoeStyle(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Color(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)
    hexCode = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Wallet(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)
    balance = models.IntegerField()

    # Foreign key.
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=0)
    # FIXME: This default value is not good setting.


class TransactionLog(models.Model):

    ''' Models' settings. '''
    datetime = models.DateTimeField()
    amount = models.IntegerField()
    log = models.CharField(max_length=100)

    # Foreign key.
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE)


class Bank(models.Model):

    ''' Models' settings. '''
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)


class BankAccount(models.Model):

    ''' Models' settings. '''
    accountName = models.CharField(max_length=50)
    account = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)

    # Foreign key.
    bank = models.ForeignKey('Bank', on_delete=models.CASCADE)
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE)




class Post(models.Model):

    ''' Models' settings. '''
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    time = models.TimeField()
    isProduct = models.BooleanField(default=False)

    # Foreign key.
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # product


class Comment(models.Model):

    ''' Models' settings. '''
    text = models.TextField()
    time = models.TimeField()

    # Foreign key.
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)


class Like(models.Model):

    # Foreign key
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)



class Recognization(models.Model):

    ''' Models' settings. '''
    # FIXME: this is model need to set
    pass



# FIXME: all content about forum should use aldryn_newsblog or something else.


class DNNModelTester(models.Model):
    # This model is created for testing ai models, should be remove.
    # FIXME: remove this model after testing connect ai model.
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')

