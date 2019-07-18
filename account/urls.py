from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

# app_name = 'account'

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('password_change_done')), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('register/', views.register, name='register'),
    path('share/', views.share, name='share'),
    path('like/', views.like, name='like'),
    path('post_comment/', views.post_comment, name='post_comment'),
    path('comment/', views.comment, name='comment'),
    path('edit/', views.edit, name='edit'),
    path('my_fans/', views.my_fans, name='my_fans'),
    path('my_follow/',views.my_follow, name='my_follow'),
    path('bulletin/<id>', views.bulletin, name='bulletin'),
    path('users/follow/', views.user_follow, name="user_follow"),
    path('users/delmsg/', views.del_msg, name="del_msg"),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
