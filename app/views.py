
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import View
from django.views.generic.edit import CreateView, FormView, UpdateView

from .Forms import StyleForm, UserForm
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

    def get(self, request):
        auth.logout(request)
        return redirect(reverse('home'))

# 註冊頁
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password2']
            user = authenticate(request, username=username, password=password)

            return redirect(reverse('login'))

    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'app/Register.html', context=context)



# 使用者資料編輯頁
class EditUserView(UpdateView):
    model = User
    fields = ['username', 'email', 'nickname', 'phone']
    template_name = 'app/EditUser.html'

    def get_success_url(self):
        return reverse('home')

<<<<<<< HEAD
=======

>>>>>>> 57216f66e6bc83ea0b2cee6cd24da5c0d03e9729
# 忘記密碼頁
class ForgetPasswordView():
    pass


