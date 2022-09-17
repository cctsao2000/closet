
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

from .models import Bank, BankAccount, Clothe, User, DNNModelTester, Color, Style, Type, \
                    Company, Post, Comment, SecondHandPost, Cart, SecondHandComment, \
                    Closet, TransactionLog, Outfit, Wallet, SimilarityModel

# ImportError: cannot import name 'Classifier' from 'app.ai_models'
# from .ai_models import Classifier
from .ai_models.tc_loadmodel import loadClassifyModel, colorClassify
from .ai_models import findsimilar

from pathlib import Path
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


# 探索穿搭頁面
class PostView(ListView):
    model = Post
    template_name = 'app/SearchOutfits.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user_closets = Closet.objects.filter(user_id=self.request.user.id)
        context['user_closets'] = user_closets
        return context

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

        return redirect(reverse('posts'))




# Remake Outfits
def remakeOutfits(request, postPk):
    user = request.user
    post = Post.objects.get(id=postPk)
    user_closets = Closet.objects.filter(user_id=user.id)
    return render(request, 'app/RemakeOutfits.html', context={'post': post, 'user_closets': user_closets})


class CreatePostView(CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'app/AddNewOutfit.html'

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
        user = request.user
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

        return redirect(reverse('viewPost', kwargs={'postPk': _post.id}))

    return render(request, 'app/BrowseMyOutfit.html', context={'post': _post})

def view_comment(request, postPk):
    _post = Post.objects.get(id=postPk)

    def post(self, request):
        user = request.user
        _post = Post.objects.get(id=request.POST['post_id'])
        comment = request.POST.get('comment', None)
        time = arrow.now()
        print('c', comment)
        if comment:
            new_comment = Comment(text=comment, time=time.format('HH:MM'), user=user)
            new_comment.save()
            _post.comments.add(new_comment)
            _post.save()

        return redirect(reverse('viewComment', kwargs={'postPk': _post.id}))

    return render(request, 'app/Comments.html', context={'post': _post})


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
                return redirect(reverse('clothe',  kwargs={'closetPk': user.closet_set.first().id}))

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
def profile(request, closetPk):
    user = request.user
    posts = Post.objects.filter(user=user)
    user_closets = Closet.objects.filter(user_id=user.id)
    return render(request, 'app/Personal.html', context={'posts': posts, 'user_closets': user_closets})


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

    def get_queryset(self):
        closet_id = self.kwargs.get('closetPk', None)
        queryset = Closet.objects.get(id=closet_id).clothes.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        user_closets = Closet.objects.filter(user_id=user.id)
        types = Type.objects.all()
        clothes = Clothe.objects.filter(user_id=self.request.user.id)

        context['user_closets'] = user_closets
        context['types'] = types
        context['clothes'] = clothes

        # Every types of clothes
        t_shirts = Clothe.objects.filter(user_id=user.id).filter(type_id=2)
        shirts = Clothe.objects.filter(user_id=user.id).filter(type_id=1)
        shorts = Clothe.objects.filter(user_id=user.id).filter(type_id=4)
        pants = Clothe.objects.filter(user_id=user.id).filter(type_id=3)
        skirts = Clothe.objects.filter(user_id=user.id).filter(type_id=5)
        dresses = Clothe.objects.filter(user_id=user.id).filter(type_id=6)
        shoes = Clothe.objects.filter(user_id=user.id).filter(type_id=7)

        context['t_shirts'] = t_shirts
        context['shirts'] = shirts
        context['shorts'] = shorts
        context['pants'] = pants
        context['skirts'] = skirts
        context['dresses'] = dresses
        context['shoes'] = shoes

        return context

# 衣物管理 - 讀取單一衣物種類頁面
class ShowSingleClotheView(ListView):
    model = Clothe
    template_name = 'app/Tshirt.html'
    paginate_by = 4

    def get_queryset(self):
        closet_id = self.kwargs.get('closetPk', None)
        queryset = Closet.objects.get(id=closet_id).clothes.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        user_closets = Closet.objects.filter(user_id=self.request.user.id)
        type = Type.objects.get(id=self.kwargs.get('typePk', None))
        clothes = user_closets.get(id=self.kwargs.get('closetPk', None)).clothes.filter(type_id=type.id)

        context['user_closets'] = user_closets
        context['type'] = type
        context['clothes'] = clothes

        return context

class CreateSubClosetView(CreateView):
    model = Closet
    template_name = 'app/CreateSubCloset.html'
    fields = ['user', 'name', 'clothes']

    def get_success_url(self):
        user_closets = Closet.objects.filter(user_id=self.kwargs.get('userPk', None))
        return reverse(
            'clothe',
            kwargs={
                'closetPk': user_closets.first().id,
            }
        )



def show_single_clothe(request, closetPk, clothePk):
    closet = Closet.objects.get(id=closetPk)
    clothe = Clothe.objects.get(id=clothePk)
    related_posts = Post.objects.filter(clothes__in=[clothe])

    context={
        'closet': closet,
        'clothe': clothe,
        'related_posts': related_posts,
    }

    return render(request, 'app/BrowseMyClothes.html', context=context)

# 7/25
def outfit(request, closetPk):
    user = request.user
    user_closets = Closet.objects.filter(user_id=user.id)
    posts = Post.objects.filter(user=user)

    return render(request, 'app/MyOutfits.html', context={'posts': posts, 'user_closets': user_closets})

def saved_outfit(request, closetPk):
    user_closets = Closet.objects.filter(user_id=request.user.id)
    return render(request, 'app/SaveOutfits.html', context={'user_closets': user_closets})


''' 分隔線 '''


# 衣物管理 - 新增頁面
class CreateClotheView(CreateView):
    model = Clothe
    fields = ['image']
    template_name = 'app/AddNewClothes.html'

    def post(self, request, *args, **kwargs):
        return CreateView.post(self, request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'editClothe',
            kwargs={
                'pk': self.object.id,
                'closetPk': self.object.closet_set.first().id
            }
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['styles'] = Style.objects.all()
        context_data['colors'] = Color.objects.all()
        context_data['types'] = Type.objects.all()
        context_data['companies'] = Company.objects.all()
        user_closets = Closet.objects.filter(user_id=self.request.user.id)
        context_data['user_closets'] = user_closets

        return context_data

    def form_valid(self, form):
        self.object = form.save()
        obj = self.object
        obj.closet_set.add(self.request.user.closet_set.first())
        if self.request.POST.get('new_image'):
            predict_image(obj)
        obj.save()

        return HttpResponseRedirect(self.get_success_url())


def predict_image(obj):
    # FIXME: 最好調整一下 CLASSIFIER 的操作，這樣不好用，而且現在的 code 好醜，跟瀞之討論之後再看看怎麼調是最好的
    img_path = Clothe.objects.get(id=obj.id).image.path
    pred_type_result = loadClassifyModel(img_path)
    pred_color_result = colorClassify(img_path)
    pred_result = {
        'type': CONVERT_PREDICT_TYPE[pred_type_result],
        'color': CONVERT_PREDICT_COLOR[pred_color_result]
    }
    print(CONVERT_PREDICT_COLOR[pred_color_result])
    obj.color.add(Color.objects.get(id=pred_result['color']))
    obj.type = Type.objects.get(id=pred_result['type'])

    obj.save()


# 衣物管理 - 編輯頁面
class EditClotheView(UpdateView):
    model = Clothe
    fields = ['name', 'image', 'isFormal', 'warmness', 'color', 'company', 'style', 'shoeStyle', 'type', 'note']
    template_name = 'app/AddNewClothes.html'
    context_object_name = 'clothe'
    # template_name = 'app/EditClothes.html'

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
            'viewClothe',
            kwargs={
                'closetPk': self.request.user.closet_set.first().id, # FIXME: self.object.closet_set.first().id,
                'clothePk': self.object.id,
            },
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
        return reverse('clothe', kwargs={'closetPk': self.request.user.closet_set.first().id})


# Revision Needed
# 穿搭推薦
class RecommendView(View):

    def get(self, request):
        # refreshSimilarityModel(request)
        return render(request, 'app/Recommend.html')

    def get_success_url(self):
        return reverse('recommend')

def refreshSimilarityModel(request):
    user = request.user
    model = Clothe.objects.filter(user=user).first()
    path = Path(model.image.path)
    print(path.parent.absolute())
    findsimilar.refreshSimilarityModel(path.parent.absolute(), user.id)


# 用戶設定
class SettingView(View):

    def get(self, request):
        return render(request, 'app/Setting.html')

    def get_success_url(self):
        return reverse('setting')


''' 二手拍頁面 '''


# class SecondHandPostListView(ListView):

#     model = SecondHandPost
#     paginate_by = 100
#     template_name = 'app/SecondhandIndex1.html'

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         title = self.request.GET.get('title', None)
#         if title:
#             queryset = queryset.filter(title__contains=title)
#         return queryset


# class SecondHandPostDetailView(DetailView):

#     model = SecondHandPost
#     template_name = 'app/GoodsPage.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         comments = list(SecondHandComment.objects.filter(post=post))
#         context['comments'] = comments
#         return context

    # # FIXME: 想一想之後還是覺得這個應該要拆開來用不同的 View 做才對。
    # def post(self, request):
    #     user = request.user
    #     _post = SecondHandPost.objects.get(id=request.POST['post_id'])
    #     comment = request.POST.get('comment', None)
    #     like = request.POST.get('like', None)
    #     followed = request.POST.get('followed', None)
    #     time = arrow.now().datetime

    #     if comment:
    #         new_comment = SecondHandComment(text=comment, time=time, user=user)
    #         new_comment.save()
    #         _post.comments.add(new_comment)
    #         _post.save()

    #     if like:
    #         _post.likes.add(user)
    #         _post.save()

    #     if followed:
    #         user.followedPosts.add(_post)
    #         user.save()

    #     return reverse('secondehand')

def get_good_management_page(request):
    posts = SecondHandPost.objects.filter(user=request.user)
    context = {'posts': posts}

    return render(request, 'app/GoodManage.html', context=context)


def list_goods(request):
    posts = SecondHandPost.objects.filter(isSold=False).exclude(user=request.user).order_by('-id')
    context = {'posts': posts}
    return render(request, 'app/SearchGoods.html', context=context)


def get_secondhand_post(request, pk):
    post = SecondHandPost.objects.get(id=pk)
    prob_like_posts = SecondHandPost.objects.filter(
        product__style=post.product.style.first(),
        product__warmness=post.product.warmness,
    ).exclude(user=request.user)
    context = {
        'post': post,
        'prob_like_posts': prob_like_posts,
    }
    return render(request, 'app/Good.html', context=context)


def get_secondhand_comments(request, pk):
    comments = SecondHandComment.objects.filter(post=pk)
    context = {'comments': comments}
    return render(request, 'app/XXXX.html', context=context)


def get_my_single_secondhand(request, pk):
    post = SecondHandPost.objects.get(id=pk)
    context = {
        'post': post,
    }
    return render(request, 'app/BrowseMyGoods.html', context=context)


class SecondHandPostCreateView(CreateView):

    form_class = SecondHandPostForm
    template_name = 'app/AddGoods.html'

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
        return reverse('mysecondhand')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clothe = Clothe.objects.get(id=self.kwargs.get('clothePk'))
        context['clothe'] = clothe
        context['my_posts'] = clothe.post_set.all()
        return context


class SecondHandPostUpdateView(UpdateView):

    model = SecondHandPost
    template_name = 'app/EditGoods.html'
    fields = ['title', 'content']

    def get_success_url(self):
        return reverse('clothe', kwargs={'closetPk': self.request.user.closet_set.first().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clothe'] = Clothe.objects.get(id=self.object.product.id)
        return context


class SecondHandPostDeleteView(DeleteView):

    # TODO: integrate front-end.
    model = SecondHandPost
    template_name = 'app/_editSecondHandPost.html'

    def get_success_url(self):
        return reverse('clothe', kwargs={'closetPk': self.request.user.closet_set.first().id})


''' 購物車頁面（交易相關） '''
class CartListView(ListView):

    # TODO: integrate front-end.
    model = Cart
    template_name = 'app/MyShoppingCart.html'
    context_object_name = 'carts'

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
        prev_page = self.request.GET.get('prevPage')
        if prev_page:
            return prev_page
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
        selected_carts = request.POST.get('selected_carts', '')
        selected_carts = selected_carts.split(',')
        selected_carts = Cart.objects.filter(id__in=selected_carts)
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
            product.user = buyer
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

        return redirect('cart_list')


def get_transaction_log(request):
    logs = TransactionLog.objects.filter(wallet__user=request.user)
    context = {'logs': logs}
    return render(request, 'app/Transactionlog.html', context=context)


def get_my_wallet(request):
    wallet = Wallet.objects.get(user=request.user)
    context = {'wallet': wallet}
    return render(request, 'app/MyWallet.html', context=context)


def set_my_wallet(request):
    wallet = Wallet.objects.get(user=request.user)
    bankaccounts = BankAccount.objects.filter(wallet__user=request.user)
    context = {
        'wallet': wallet,
        'bankaccounts': bankaccounts,
    }
    return render(request, 'app/WalletSetting.html', context=context)





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
