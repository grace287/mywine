from django.db import models
from django.conf import settings
from notes.models import TastingNote
from django.contrib.auth import get_user_model

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tasting_note = models.ForeignKey(
        'notes.TastingNote',  # 문자열로 참조
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    POST_TYPES = (
        ('review', '시음 후기'),
        ('event', '이벤트/모임'),
        ('discussion', '자유토론'),
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts')
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participating_events')
    max_participants = models.PositiveIntegerField(default=0)  # 0은 제한없음
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['event_date']

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    posts = models.ManyToManyField(Post, related_name='tags')

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_important = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_important', '-created_at']

    def __str__(self):
        return self.title
