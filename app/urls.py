from django.conf.urls.static import static
from django.urls import path
from AppServer import settings
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
    path('forgetpassword', views.ForgetPasswordView.as_view(), name='forgetPassword'),
    path('profile', views.ProfileView.as_view(), name='profile'),

    # 衣物管理
    path('clothes', views.ShowClotheView.as_view(), name='clothe'),
    path('clothes/create', views.CreateClotheView.as_view(), name='createClothe'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

