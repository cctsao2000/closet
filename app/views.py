
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView, View

from .Forms import StyleForm, UserForm, DNNForm

from .models import Clothe, User, DNNModelTester, Color, Style, Type, Company, Post, Comment


from .ai_models import Classifier

import arrow

# Create your views here.

CONVERT_PREDICT_COLOR = {
    'Black': 1,
    'White': 2,
    'Blue': 3,
    'Brown': 4,
    'Grey': 5,
    'Red': 6,
    'Green': 7,
    'Navy Blue': 8,
    'Pink': 9,
    'Purple': 10,
    'Silver': 11,
    'Yellow': 12,
    'Beige': 13,
    'Gold': 14,
    'Maroon': 15,
    'Orange': 16,
    'Other': 17
}

CONVERT_PREDICT_TYPE = {
    'shirt': 1,
    'tshirt': 2,
    'pants': 3,
    'shorts': 4,
    'skirt': 5,
    'dress': 6,
    'footwear': 7
}

# 首頁
class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'app/index.html'

    def post(self, request):
        _post = Post.objects.get(id=request.POST['post_id'])
        comment = request.POST['comment']
        time = arrow.now()

        if comment:
            new_comment = Comment(text=comment, time=time.format('HH:MM'), user=request.user)
            new_comment.save()
            _post.comments.add(new_comment)
            _post.save()

        return render(request, 'app/index.html')



class SinglePostView(DetailView):
    model = Post
    template_name = 'app/SinglePost.html'


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
class ProfileView(ListView):
    model = Post
    template_name = 'app/Profile.html'
    paginate_by = 9

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)



# 使用者資料編輯頁
class EditUserView(UpdateView):
    model = User
    fields = ['nickname', 'profile_picture', 'biography']
    template_name = 'app/ProfileEdit.html'

    def get_success_url(self):
        return reverse(
            'profile',
            kwargs={
                'pk': self.object.id,
            }
        )



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
    template_name = 'app/ClosetSetting.html'
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

    def form_valid(self, form):
        # FIXME: 新增一個 ClotheForm，把這邊搬過去 form.save() 裡面。
        # 另外，因為之後可能會改成圖片去背完再儲存，這也需要放到 form.save() 裡面。
        self.object = form.save()

        object = self.object
        user_pk = self.kwargs.get('userPk')
        object.closet_set.add(User.objects.get(id=user_pk).closet_set.first())

        if self.request.POST.get('new_image'):
            predict_image(object)
        object.save()

        return HttpResponseRedirect(self.get_success_url())


def predict_image(object):
    classifier = Classifier()
    img_path = Clothe.objects.get(id=object.id).image.path
    pred_type_result = classifier.pred_type(img_path)
    pred_color_result = classifier.pred_color(img_path)
    pred_result = {
        'type': CONVERT_PREDICT_TYPE[pred_type_result],
        'color': CONVERT_PREDICT_COLOR[pred_color_result]
    }
    object.color.add(Color.objects.get(id=pred_result['color']))
    object.type = Type.objects.get(id=pred_result['type'])
    object.save()


# 衣物管理 - 編輯頁面
class EditClotheView(UpdateView):
    model = Clothe
    fields = ['name', 'image', 'isFormal', 'warmness', 'color', 'company', 'style', 'shoeStyle', 'type', 'note']
    template_name = 'app/ClosetSetting.html'

    def form_invalid(self, form):
        if not form.cleaned_data['image']:
            form.cleaned_data['image'] = self.get_object().image
        return UpdateView.form_invalid(self, form)

    def form_valid(self, form):
        # FIXME: 同 CreateClotheView.form_valid()
        self.object = form.save()
        object = self.object

        if self.request.POST.get('new_image'):
            predict_image(object)

        return HttpResponseRedirect(self.get_success_url())

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
    pred_results = {'type': pred_type_result, 'color': pred_color_result}

    return render(request, 'app/DNNModelTester.html', {'result': pred_results})
