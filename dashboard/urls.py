from django.urls import path
from . import views

app_name = 'dashboard' # app_name 추가

urlpatterns = [
    # path('', views.dashboard_view, name='dashboard'),  # 대시보드 메인 페이지
    path('filter/', views.filter_results, name='filter_results'),  # 필터 결과 페이지
    path('statistics', views.statistics, name='statistics'),
]