from django.contrib import admin
from .models import Clothe, Color, Company, ShoeStyle, Style, Type, User

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

