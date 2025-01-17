from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_important', 'created_at', 'views')
    list_filter = ('is_important', 'created_at')
    search_fields = ('title', 'content')
    
    # 작성자를 자동으로 현재 관리자로 설정
    def save_model(self, request, obj, form, change):
        if not change:  # 새로운 공지사항 작성 시
            obj.author = request.user
        obj.save()
