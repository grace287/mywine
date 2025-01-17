from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'회원가입이 완료되었습니다. {username}님 환영합니다! 로그인해주세요.')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next', 'home')
            messages.success(request, f'{username}님 환영합니다!')
            return redirect(next_url)
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
    return render(request, 'users/login.html')

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def profile_edit(request):
    # 항상 user_form 초기화
    user_form = UserUpdateForm(instance=request.user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            messages.success(request, '프로필이 성공적으로 업데이트되었습니다.')
            # 명시적으로 리다이렉트 URL 지정
            return redirect(reverse('users:profile'))
        else:
            messages.error(request, '프로필 업데이트 중 오류가 발생했습니다.')
    else:
        # GET 요청시에는 둘 다 보여주되 user_form은 읽기 전용으로
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, 'users/profile_edit.html', context)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'register/password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'register/password_reset_email.html'
    subject_template_name = 'register/password_reset_subject.txt'
    html_email_template_name = 'register/password_reset_email.html'