from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_home, name='home'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/update/', views.post_update, name='post_update'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('share-note/<int:note_id>/', views.share_tasting_note, name='share_note'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
] 