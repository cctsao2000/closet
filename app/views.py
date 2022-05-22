
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView, View
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView

from .Forms import StyleForm, UserForm, DNNForm

from .models import Clothe, User, DNNModelTester, Color, Style, Type, Company, Post


from .ai_models import Classifier

import arrow

# Create your views here.



# 首頁
class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'app/index.html'


class CreatePostView(CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'app/WritePosts.html'
    
    def post(self, request, *args, **kwargs):
        content = request.POST['content']
        tag = request.POST['title']
        image = request.POST['image']
        time = arrow.now()

        new_post = Post(title=tag, content=content, image=image, time=time.format('HH:MM'), user=request.user)
        new_post.save()
        
        return render(request, 'app/index.html')
    
    def get_success_url(self):
        return reverse('home')
    


# 登入頁
class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
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
            message = '登入失敗，請確認帳號與密碼後重新嘗試！'
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
    return render(request, 'app/SignUp.html', context=context)


''' 分隔線 單純因為摺疊程式碼不想被咖到下面這行註解 可刪 '''
# 個人頁面
class ProfileView(View):
    # FIXME: 這個有問題，不應該這樣寫，應該要用 generic view 的方式，而不是 override 掉他的 get
    # 而且這樣沒有 user id，跟實際上應該要的流程不一樣
    def get(self, request):
        return render(request, 'app/Profile.html')



# 使用者資料編輯頁
class EditUserView(UpdateView):
    model = User
    fields = ['username', 'email', 'nickname', 'phone']
    template_name = 'app/ProfileEdit.html'

    def get_success_url(self):
        return reverse('profile')



# 忘記密碼頁
class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'app/ForgotPassword.html')

    def post(self, request):
        email = request.POST['email']
        user = User.objects.get(email=email)
        if user:
            print('send email')
            send_mail(
                '這是一封驗證信',
                '這是驗證信的內容',
                'nccumis@nccu.edu.tw',
                [email],
            )
        else:
            pass
        return redirect(reverse('login'))


# 衣物管理 - 讀取頁面
class ShowClotheView(ListView):
    model = Clothe
    template_name = 'app/MyCloset.html'
    paginate_by = 4

''' 分隔線 '''
# 衣物管理 - 新增頁面
class CreateClotheView(CreateView):
    model = Clothe
    fields = ['image']
    template_name = 'app/CreateClothe.html'

    def get_success_url(self):
        return reverse(
            'editClothe',
            kwargs={
                'pk': self.object.id,
                'userPk': self.object.closet_set.first().user
            }
        )

    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        context_data['styles'] = Style.objects.all()
        context_data['colors'] = Color.objects.all()
        context_data['types'] = Type.objects.all()
        context_data['companies'] = Company.objects.all()

        return context_data

# 衣物管理 - 編輯頁面
class EditClotheView(UpdateView):
    model = Clothe
    fields = ['name', 'image', 'isFormal', 'warmness', 'color', 'company', 'style', 'shoeStyle', 'type', 'note']
    template_name = 'app/ClosetSetting.html'

    def form_invalid(self, form):
        if not form.cleaned_data['image']:
            form.cleaned_data['image'] = self.get_object().image
        return UpdateView.form_invalid(self, form)

    def get_success_url(self):
        return reverse(
            'editClothe',
            kwargs={
                'pk': self.object.id,
                'userPk': self.object.closet_set.first().user.id
            }
        )

    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        context_data['styles'] = Style.objects.all()
        context_data['colors'] = Color.objects.all()
        context_data['types'] = Type.objects.all()
        context_data['companies'] = Company.objects.all()

        return context_data

# 衣物管理 - 刪除頁面
class DeleteClotheView(DeleteView):
    model = Clothe
    template_name = 'app/DeleteClothe.html'

    def get_success_url(self):
        return reverse('courseView')

# Revision Needed
# 穿搭推薦
class RecommendView(View):
    def get(self, request):
        return render(request, 'app/Recommend.html')

    def get_success_url(self):
        return reverse('recommend')

# 用戶設定
class SettingView(View):
    def get(self, request):
        return render(request, 'app/Setting.html')

    def get_success_url(self):
        return reverse('setting')

''' Model AJAX. '''
def get_model_predict(request, pk):

    if request.method == 'POST':
        classifier = Classifier()
        img_path = DNNModelTester.objects.get(id=pk).image.path
        type_ = classifier.pred_type(img_path)
        color = classifier.pred_color(img_path)
        result = {
            'type': type_,
            'color': color,
        }
        return JsonResponse(result)
    else:
        raise PermissionDenied


''' Model test. '''
# Create your views here.
def DNN_model_tester_view(request):

    if request.method == 'POST':
        form = DNNForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.save()
            return redirect('success', pk=image.id)
    else:
        form = DNNForm()
    return render(request, 'app/DNNModelTester.html', {'form' : form})


def success(request, pk):

    classifier = Classifier()
    img_path = DNNModelTester.objects.get(id=pk).image.path
    pred_type_result = classifier.pred_type(img_path)
    pred_color_result = classifier.pred_color(img_path)
    pred_results = [pred_type_result, pred_color_result]

    return render(request, 'app/DNNModelTester.html', {'result': pred_results})
