
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import View
from django.views.generic.edit import CreateView, FormView

from .Forms import StyleForm
from .models import User

# Create your views here.



# 首頁
class HomeView(View):

    def get(self, request):
        return render(request, 'app/Home.html')



# 登入頁
class LoginView(View):

    def get(self, request):
        return render(request, 'app/Login.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home'))

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            # 登入成功 導向首頁
            if user.is_active:
                message = '登入成功！'
                messages.add_message(request, messages.SUCCESS, message)
                return redirect(reverse('home'))

            # 第一次登入成功 導向風格頁面
            else:
                message = '首次登入，請完成風格測驗！'
                messages.add_message(request, messages.SUCCESS, message)
                return redirect(reverse('styleForm'))

        # 登入失敗
        else:
            return render(request, 'app/Login.html', locals())



# 風格測驗
class StyleFormView(FormView):

    form_class = StyleForm
    template_name = 'app/StyleForm.html'

    def form_valid(self, form):
        form.saveResult()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')

# 登出頁
class LogoutView(View):

    def post(self, request):
        auth.logout(request)
        return redirect(reverse('home'))



# 註冊頁
class RegisterView(CreateView):

    model = User
    fields = []
    template_name = 'app/Register.html'

    def get_success_url(self):
        return reverse('home')



# 忘記密碼頁
class ForgetPasswordView():
    pass


