from django.urls import path
from . import views

app_name = 'gallery' # app_name 추가

urlpatterns = [
    path('', views.gallery_view, name='gallery_view'),
]