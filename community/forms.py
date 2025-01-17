from django import forms
from .models import Post, Comment, Event, Notice

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '내용을 입력하세요'
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'post_type': '게시글 유형'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '댓글을 입력하세요'
            })
        }
        labels = {
            'content': '댓글'
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'event_date', 'max_participants']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '이벤트 제목을 입력하세요'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '이벤트 설명을 입력하세요'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '장소를 입력하세요'
            }),
            'event_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0은 제한없음'
            })
        }
        labels = {
            'title': '이벤트 제목',
            'description': '이벤트 설명',
            'location': '장소',
            'event_date': '일시',
            'max_participants': '최대 참가 인원'
        }
        help_texts = {
            'max_participants': '0으로 설정하면 인원 제한이 없습니다.'
        }

    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date and event_date < timezone.now():
            raise forms.ValidationError('과거의 날짜는 선택할 수 없습니다.')
        return event_date 

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'is_important']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '공지사항 제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '공지사항 내용을 입력하세요',
                'rows': 10
            }),
            'is_important': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'is_important': '중요 공지'
        } 