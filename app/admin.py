from django.contrib import admin
from .models import Clothe, Closet, Color, Company, Comment, Post, ShoeStyle, Style, Type, User, Wallet, SecondHandPost

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email', 'nickname', 'phone']
    list_filter = ('id', 'username')
    list_display = ('id', 'username', 'nickname', 'phone')

@admin.register(Clothe)
class ClotheAdmin(admin.ModelAdmin):
    search_fields = ['name', 'isFormal', 'warmness']
    list_filter = ('id', 'name')
    list_display = ('id', 'name', 'isFormal', 'warmness')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'time']
    list_filter = ('id', 'title')
    list_display = ('id', 'title', 'time')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['text', 'time']
    list_filter = ('id', 'text')
    list_display = ('id', 'text', 'time')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('id', 'name')
    list_display = ('id', 'name')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('id', 'name')
    list_display = ('id', 'name')

@admin.register(ShoeStyle)
class ShoeStyleAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('id', 'name')
    list_display = ('id', 'name')

@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('id', 'name')
    list_display = ('id', 'name')

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('id', 'name')
    list_display = ('id', 'name')

@admin.register(Closet)
class ClosetAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = [field.name for field in Closet._meta.fields]

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['name', 'balance', 'user']

@admin.register(SecondHandPost)
class SecondHandPost(admin.ModelAdmin):
    list_display = ['title', 'content', 'time', 'used', 'isProduct', 'amount', 'user', 'product']
