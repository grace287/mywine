from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='users:login',
        template_name='users/login.html'
    ), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # 비밀번호 재설정 관련 URL 패턴들
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='register/password_reset.html',
             email_template_name='register/password_reset_email.html',
             subject_template_name='register/password_reset_subject.txt',
             success_url='/users/password_reset/done/'
         ),
         name='password_reset'),
         
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='register/password_reset_done.html'
         ),
         name='password_reset_done'),
         
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='register/password_reset_confirm.html',
             success_url='/users/reset/done/'
         ),
         name='password_reset_confirm'),
         
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='register/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]