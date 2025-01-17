from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import landing_page

urlpatterns = [
    path('', landing_page, name='landing'),  # 기존 TemplateView를 커스텀 뷰로 변경
    # path('', TemplateView.as_view(template_name='landing.html'), name='landing'),  # 추가
    path('admin/', admin.site.urls),
    
    path('social-auth/', include('social_django.urls', namespace='social')),
    
    # notes 앱의 URL
    path('notes/', include('notes.urls', namespace='notes')),
    path('users/', include('users.urls', namespace='users')),
    path('gallery/', include('gallery.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('community/', include('community.urls')),
    
    # 로그인 관련 URL
    path('login/', RedirectView.as_view(pattern_name='users:login'), name='login'),
    path('logout/', RedirectView.as_view(pattern_name='users:logout'), name='logout'),
    
    # 홈페이지는 notes:home_default로 리다이렉트
    path('', RedirectView.as_view(pattern_name='notes:home_default'), name='home'),
]
# 미디어 파일 서빙 설정
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)