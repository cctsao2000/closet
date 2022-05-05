
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.http import HttpResponse # TODO: Should be remove after testing DNNModel.
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView, View
from django.views.generic.edit import CreateView, FormView, UpdateView

from .Forms import StyleForm, UserForm, DNNForm
from .models import Clothe, User, DNNModelTester

# from .ai_models import Classifier

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
        form.save_result()
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



# 個人頁面
class ProfileView(View):

    def get(self, request):
        return render(request, 'app/Profile.html')



# 使用者資料編輯頁
class EditUserView(UpdateView):
    model = User
    fields = ['username', 'email', 'nickname', 'phone']
    template_name = 'app/EditUser.html'

    def get_success_url(self):
        return reverse('profile')



# 忘記密碼頁
class ForgetPasswordView(View):

    def get(self, request):
        return render(request, 'app/ForgetPassword.html')


# 衣物管理 - R 頁面
class ShowClotheView(ListView):
    model = Clothe
    template_name = 'app/Clothes.html'
    paginate_by = 4


# 衣物管理 - C 頁面
class CreateClotheView(CreateView):
    model = Clothe
    fields = ['name', 'image', 'isFormal', 'warmness', 'color', 'company', 'style', 'shoeStyle', 'type']
    template_name = 'app/CreateClothe.html'

    def get_success_url(self):
        return reverse('clothe')



# ''' Model test. '''
# # Create your views here.
# def DNN_model_tester_view(request):

    # if request.method == 'POST':
        # form = DNNForm(request.POST, request.FILES)

        # if form.is_valid():
            # image = form.save()
            # return redirect('success', pk=image.id)
    # else:
        # form = DNNForm()
    # return render(request, 'app/DNNModelTester.html', {'form' : form})


# def success(request, pk):

    # classifier = Classifier()
    # predict_result = classifier.predict(DNNModelTester.objects.get(id=pk).image.path)

    # return HttpResponse(predict_result)

def test(request):

    return render(request, 'app/cameraApp.html')

def camerawork(request):
    
    return HttpResponse('camerawork')