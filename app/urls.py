from django.conf.urls.static import static
from django.urls import path
from AppServer import settings
from . import views


urlpatterns = [

    # 首頁
    path('', views.HomeView.as_view(), name='home'),
    path('<int:userPk>/closet/create', views.CreateSubClosetView.as_view(), name='createCloset'),
    path('<int:userPk>/posts/create', views.CreatePostView.as_view(), name='createPost'),
    # 6/18 added
    path('posts/<int:postPk>', views.view_post, name='viewPost'),
    path('posts/<int:postPk>/comments', views.view_comment, name='viewComment'),
    path('<int:userPk>/posts/<int:postPk>/edit', views.EditPostView.as_view(), name='editPost'),
    # 8/21 added, need to remove the home page and replace with this page in the next version
    path('posts', views.PostView.as_view(), name='posts'),
    # 復刻圖片
    path('posts/<int:postPk>/remake', views.remakeOutfits, name='remake'),

    # 登入登出、註冊、風格測驗
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('signup', views.register, name='signup'),
    path('styleform', views.StyleFormView.as_view(), name='styleForm'),
    path('<int:pk>/edit', views.EditUserView.as_view(), name='editUser'),
    path('forgotpassword', views.ForgotPasswordView.as_view(), name='forgotPassword'),
    # 6/18 edited
    path('<int:closetPk>/profile', views.profile, name='profile'),

    # 衣物管理
    path('<int:closetPk>/clothes', views.ShowClotheView.as_view(), name='clothe'),
    path('<int:closetPk>/clothes/create', views.CreateClotheView.as_view(), name='createClothe'),
    path('<int:closetPk>/clothes/<int:clothePk>', views.show_single_clothe, name='viewClothe'),
    path('<int:closetPk>/clothes/<int:pk>/edit', views.EditClotheView.as_view(), name='editClothe'),
    path('<int:closetPk>/clothes/<int:pk>/delete', views.DeleteClotheView.as_view(), name='deleteClothe'),

    path('<int:closetPk>/clothes/type/<int:typePk>', views.ShowSingleClotheView.as_view(), name='single_clothe'),
    path('<int:closetPk>/outfits', views.outfit, name='outfit'),
    path('<int:closetPk>/savedoutfits', views.saved_outfit, name='savedOutfit'),

    # 穿搭推薦
    path('recommend', views.RecommendView.as_view(), name='recommend'),

    # 二手
    path('mysecondhand', views.get_good_management_page, name='mysecondhand'),
    path('secondhand', views.list_goods, name='secondhand_list'),
    path('secondhand/<int:pk>', views.get_secondhand_post, name='secondhand'),
    path('secondhand/<int:pk>/comments', views.get_secondhand_comments, name='secondhand_comments'),
    path('secondhand/<int:clothePk>/create', views.SecondHandPostCreateView.as_view(), name='secondhandCreate'),
    path('secondhand/<int:pk>/edit', views.SecondHandPostUpdateView.as_view(), name='secondhandUpdate'),
    path('secondhand/<int:pk>/delete', views.SecondHandPostDeleteView.as_view(), name='secondhandDelete'),


    # 購物車
    path('cart', views.CartListView.as_view(), name='cart_list'),
    path('cart/<int:pk>', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/<int:pk>/delete', views.CartDeleteView.as_view(), name='cart_delete'),
    path('cart/create', views.CartCreateView.as_view(), name='cart_create'),
    path('cart/trasaction', views.CartToTransactionView.as_view(), name='cart_to_transaction'),

    # 交易紀錄
    # path(),

    # 用戶設定
    path('usersetting', views.SettingView.as_view(), name='setting'),

    # DNNModelTester.
    path('dnnmodeltester', views.DNN_model_tester_view, name='dnn_model_tester'),
    path('success/<int:pk>', views.success, name = 'success'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

