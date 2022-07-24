
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView, View
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from .Forms import StyleForm, UserForm, DNNForm, SecondHandPostForm

from .models import Clothe, User, DNNModelTester, Color, Style, Type, \
                    Company, Post, Comment, SecondHandPost, Cart, SecondHandComment, \
                    Closet, TransactionLog

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
class HomeView(ListView):
    model = Post
    template_name = 'app/index.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(request)

    def post(self, request):
        user = request.user
        _post = Post.objects.get(id=request.POST['post_id'])
        comment = request.POST.get('comment', None)
        like = request.POST.get('like', None)
        followed = request.POST.get('followed', None)
        time = arrow.now()

        if comment:
            new_comment = Comment(text=comment, time=time.format('HH:MM'), user=user)
            new_comment.save()
            _post.comments.add(new_comment)
            _post.save()

        if like:
            _post.likes.add(user)
            _post.save()

        if followed:
            user.followedPosts.add(_post)
            user.save()

        return render(request, 'app/index.html')


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


# 6/18 added
# 單一貼文瀏覽 含刪除貼文
def view_post(request, postPk):
    _post = Post.objects.get(id=postPk)

    def post(self, request):
        _post.delete()

        return redirect(reverse('index'))

    return render(request, 'app/PostPage.html', context={'post': _post})


# 6/18 added
# 編輯貼文頁
class EditPostView(UpdateView):
    model = Post
    fields = ['content', 'image']
    template_name = 'app/EditPost.html'

    def get_success_url(self):
        return reverse(
            'viewPost',
            kwargs={'postPk': self.object.id}
        )


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


# 6/18 edited 因為要列出 user 的 posts ，故改成用 view function
# 個人頁面
def profile(request, userPk):
    user = request.user
    posts = Post.objects.filter(user=user)

    return render(request, 'app/Profile.html', context={'posts': posts})


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
        context_data = super().get_context_data(**kwargs)
        context_data['styles'] = Style.objects.all()
        context_data['colors'] = Color.objects.all()
        context_data['types'] = Type.objects.all()
        context_data['companies'] = Company.objects.all()

        return context_data

    def form_valid(self, form):
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
        context_data = super().get_context_data(**kwargs)
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


''' 二手拍頁面 '''


class SecondHandPostListView(ListView):

    model = SecondHandPost
    paginate_by = 100
    template_name = 'app/SecondhandIndex1.html'
    
    
    # FIXME: 想一想之後還是覺得這個應該要拆開來用不同的 View 做才對。
    def post(self, request):
        user = request.user
        _post = SecondHandPost.objects.get(id=request.POST['post_id'])
        comment = request.POST.get('comment', None)
        like = request.POST.get('like', None)
        followed = request.POST.get('followed', None)
        time = arrow.now().datetime

        if comment:
            new_comment = SecondHandComment(text=comment, time=time, user=user)
            new_comment.save()
            _post.comments.add(new_comment)
            _post.save()

        if like:
            _post.likes.add(user)
            _post.save()

        if followed:
            user.followedPosts.add(_post)
            user.save()

        return render(request, 'app/index.html')


class SecondHandPostDetailView(DetailView):

    model = SecondHandPost
    template_name = 'app/GoodsPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = list(SecondHandComment.objects.filter(post=post))
        context['comments'] = comments
        return context


class SecondHandPostCreateView(CreateView):

    form_class = SecondHandPostForm
    template_name = 'app/ForSale.html'
    
    # FIXME: 目前還沒有做新增圖片，只有新增貼文而已，貼文的圖片還沒新增
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {'user': self.request.user}
        )
        return kwargs

    def post(self, request, *args, **kwargs):
        return super().post(self, request, *args, **kwargs)

    def get_success_url(self):
        return reverse('secondhand')


class SecondHandPostUpdateView(UpdateView):

    # TODO: integrate front-end.
    model = SecondHandPost
    template_name = 'app/_editSecondHandPost.html'
    fields = ['title', 'content']

    def get_success_url(self):
        return reverse('secondhand')


class SecondHandPostDeleteView(DeleteView):

    # TODO: integrate front-end.
    model = SecondHandPost
    template_name = 'app/_editSecondHandPost.html'

    def get_success_url(self):
        return reverse('secondhand')


''' 購物車頁面（交易相關） '''
class CartListView(ListView):

    # TODO: integrate front-end.
    model = Cart
    template_name = 'app/_cart_list.html'

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)


class CartDetailView(DetailView):

    model = Cart
    template_name = 'app/Buy.html'
    fields = '__all__'


class CartCreateView(CreateView):
    
    model = Cart
    template_name = 'app/_editSecondHandPost.html'
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('cart_list')


class CartDeleteView(DeleteView):

    # TODO: integrate front-end
    model = Cart
    template_name = 'app/XXX.html'


class CartToTransactionView(View):

    def get(self, request, *args, **kwargs):
        return redirect(reverse('cart_list'))

    def post(self, request, *args, **kwargs):
        # FIXME: 接下來要處理一些餘額不足的例外情況
        # FIXME: now I assume that one user have only one wallet,
        #        we have to handle the situation that one user have many wallets.
        # FIXME: now I assume that one user have only one closet,
        #        we have to handle the situation that one user have more than one closet.
        selected_carts = request.POST.get('selected_cart', [])
        for cart in selected_carts:
            buyer = cart.user
            seller = cart.post.user
            amount = cart.post.amount
            product = cart.post.product
            now = arrow.now().datetime

            # update wallet balance.
            buyer_wallet = Wallet.objects.filter(user=buyer).first()
            seller_wallet = Wallet.objects.filter(user=seller).first()
            buyer_wallet.balance -= amount
            seller_wallet.balance -= amount
            buyer_wallet.save()
            seller_wallet.save()

            # update the owneship of the product.
            buyer_closet = Closet.objects.filter(user=buyer).first()
            seller_closet = Closet.objects.filter(user=seller).first()
            buyer_closet.clothes.add(product)
            seller_closet.clothes.remove(product)
            buyer_closet.save()
            seller_closet.save()

            # create transaction log.
            # buyer.
            TransactionLog.objects.create(
                datetime=now,
                log=f'{buyer.nickname} 向 {seller.nickname} 購買了 {cart.post.title}',
                amount=amount,
                wallet=buyer_wallet,
                post=cart.post
            )
            # seller.
            TransactionLog.objects.create(
                datetime=now,
                log=f'{seller.nickname} 向 {buyer.nickname} 賣出了 {cart.post.title}',
                amount=amount,
                wallet=seller_wallet,
                post=cart.post
            )
            
            # delete the cart.
            cart.delete()

        return render('app/xxx.html', request)


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
    return render(request, 'app/DNNModelTester.html', {'form': form})


def success(request, pk):

    classifier = Classifier()
    img_path = DNNModelTester.objects.get(id=pk).image.path
    pred_type_result = classifier.pred_type(img_path)
    pred_color_result = classifier.pred_color(img_path)
    pred_results = {'type': pred_type_result, 'color': pred_color_result}

    return render(request, 'app/DNNModelTester.html', {'result': pred_results})
