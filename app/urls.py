
from django.urls import path

from . import views


urlpatterns = [

    # 首頁
    path('', views.HomeView.as_view(), name='home'),

    # 登入登出、註冊、風格測驗
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('register', views.register, name='register'),
    path('stylequiz', views.StyleFormView.as_view(), name='styleForm'),
    path('<int:pk>/edit', views.EditUserView.as_view(), name='editUser'),

]
