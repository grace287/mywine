from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def landing_page(request):
    # 로그인한 사용자는 홈페이지로 리다이렉트
    if request.user.is_authenticated:
        return redirect('notes:home_default')
    
    # 로그인하지 않은 사용자는 랜딩 페이지 표시
    return render(request, 'landing.html')