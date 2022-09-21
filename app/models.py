from django import forms
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
    profile_picture = models.ImageField(upload_to='images/profile_pictures', default=None, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)

    # Set REQUIRED_FIELDS.
    REQUIRED_FIELDS = []

    # Replace the USER_NAME_FIELD.
    USER_NAME_FIELD = 'username'

    # Set objects.
    objects = UserManager()

    #
    # Foreign key.
    friends = models.ManyToManyField('User')

    #
    # Followed posts.
    followedPosts = models.ManyToManyField('Post', blank=True, null=True, related_name='followers')
    followedSecondHandPosts = models.ManyToManyField('SecondHandPost', blank=True, null=True, related_name='followers')

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


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'images/user_{instance}/{filename}'


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
    # isPublic = models.BooleanField(default=False)

    # Foreign keys.
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE, blank=True, null=True)
    style = models.ManyToManyField('Style', blank=True, null=True)
    shoeStyle = models.ManyToManyField('ShoeStyle', blank=True, null=True)
    color = models.ManyToManyField('Color', blank=True, null=True)


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
    PAYMENT_CHOICES = (
        (1, '貨到付款'),
        (2, '錢包付款'),
    )

    datetime = models.DateTimeField()
    log = models.CharField(max_length=100)
    amount = models.IntegerField()
    payment = models.IntegerField(choices=PAYMENT_CHOICES)
    address = models.CharField(max_length=100)
    done = models.BooleanField()

    # Foreign key.
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE)
    post = models.ForeignKey('SecondHandPost', on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bought_transaction')
    seller = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sold_transaction')


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
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, related_name='account')


class Comment(models.Model):

    ''' Models' settings. '''
    text = models.TextField()
    time = models.TimeField()

    # Foreign key.
    user = models.ForeignKey('User', on_delete=models.CASCADE)


class Like(models.Model):

    # Foreign key
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)


class Post(models.Model):

    ''' Models' settings. '''
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    time = models.TimeField()
    isProduct = models.BooleanField(default=False)

    # Foreign key.
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    comments = models.ManyToManyField('Comment', blank=True, null=True)
    # 6/18 added
    likes = models.ManyToManyField('User', blank=True, related_name='likes')
    # 9/4 added
    clothes = models.ManyToManyField('Clothe', blank=True, null=True)


''' Models related to second hand '''


class SecondHandPost(models.Model):

    USED_CHOICES = (
        (1, 'Well-used'),
        (2, 'Used'),
        (3, 'New')
    )

    ''' Models' settings. '''
    title = models.CharField(max_length=50)
    content = models.TextField()
    isSold = models.BooleanField()
    time = models.DateTimeField(
        blank=True,
        null=True,
    )
    used = models.IntegerField(
        choices=USED_CHOICES,
        null=True,
    )
    isProduct = models.BooleanField(
        default=True,
        blank=True,
    )
    amount = models.IntegerField(
        null=True,
        blank=True,
    )

    # images.
    # image1 = models.ImageField(upload_to='images/')
    # image2 = models.ImageField(upload_to='images/')
    # image3 = models.ImageField(upload_to='images/')
    # image4 = models.ImageField(upload_to='images/')
    # image5 = models.ImageField(upload_to='images/')
    # image6 = models.ImageField(upload_to='images/')
    # image7 = models.ImageField(upload_to='images/')
    # image8 = models.ImageField(upload_to='images/')
    # image9 = models.ImageField(upload_to='images/')
    # image10 = models.ImageField(upload_to='images/')

    # Foreign key.
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    comments = models.ManyToManyField('Comment', blank=True, null=True)

    # products.
    product = models.ForeignKey('Clothe', on_delete=models.CASCADE, null=True)


class SecondHandPostImage(models.Model):

    ''' Model's settings. '''
    # image.
    image = models.ImageField(upload_to='images/')

    # foreign key.
    post = models.ForeignKey('User', on_delete=models.CASCADE, related_name='images')


class SecondHandComment(models.Model):

    text = models.TextField()
    time = models.DateTimeField()
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        'SecondHandPost',
        on_delete=models.CASCADE,
    )


class Cart(models.Model):

    ''' Model's settings. '''
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='cart'
    )

    post = models.ForeignKey(
        'SecondHandPost',
        on_delete=models.CASCADE
    )


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


class SimilarityModel(models.Model):
    userPath = models.TextField()

    similarity_model = models.FileField(upload_to=f'models/{userPath.__str__()}')

    user = models.ForeignKey('User', on_delete=models.CASCADE)


