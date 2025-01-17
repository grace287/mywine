from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('<int:year>/<int:month>/', views.home, name='home'),
    path('', views.home, name='home_default'),
    path('by-date/<str:date>/', views.notes_by_date, name='notes_by_date'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('get_events/', views.get_events, name='get_events'),
    path('counts/', views.get_note_counts, name='note_counts'),
    path('create/', views.note_create, name='note_create'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('<int:note_id>/', views.note_detail, name='note_detail'),
    path('<int:note_id>/edit/', views.note_edit, name='note_edit'),
    path('<int:note_id>/delete/', views.note_delete, name='note_delete'),
    path('search/', views.search_notes, name='search_notes'),
    path('filter/', views.filter_notes, name='filter_notes'),
    path('calendar/', views.calendar_view, name='calendar'),
    # API 엔드포인트들
    path('api/notes/<str:date_str>/', views.notes_by_date_api, name='notes_by_date_api'),
    path('api/note/<int:note_id>/', views.note_detail_api, name='note_detail_api'),
    path('search/', views.search_notes, name='search_notes'),
    path('counts/', views.get_note_counts, name='note_counts'),
    # API 엔드포인트들
    path('api/note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('api/notes/<str:date_str>/', views.notes_by_date_api, name='notes_by_date_api'),
    path('api/countries/search/', views.search_countries, name='search_countries'),
    # API 엔드포인트
    path('api/notes/<str:date_str>/', views.notes_by_date_api, name='notes_by_date_api'),
    path('api/notes/<str:date>/', views.notes_by_date_api, name='notes_by_date_api'),  # 날짜별 노트 API
    path('api/notes-by-date/<str:date>/', views.notes_by_date_api, name='notes_by_date_api'),  # 새로운 API 엔드포인트
    
    path('api/wines/search/', views.search_wines, name='search_wines'),
    path('api/test-wine/', views.test_wine_api, name='test_wine_api'),
    path('collection/', views.wine_collection, name='collection'),
]