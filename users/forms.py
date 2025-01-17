from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 에러 메시지 커스터마이징
        self.error_messages = {
            'password_mismatch': '비밀번호가 일치하지 않습니다.',
            'password_too_short': '비밀번호는 최소 8자 이상이어야 합니다.',
            'password_too_similar': '비밀번호가 개인정보와 너무 유사합니다.',
            'password_too_common': '비밀번호가 너무 일반적입니다.',
            'password_numeric': '비밀번호는 숫자로만 이루어질 수 없습니다.',
            'duplicate_username': '이미 사용 중인 아이디입니다.',
            'invalid_email': '올바른 이메일 주소를 입력해주세요.',
        }

        # 필드별 에러 메시지
        self.fields['username'].error_messages = {
            'unique': '이미 사용 중인 아이디입니다.',
            'invalid': '올바른 아이디를 입력해주세요.',
            'required': '아이디를 입력해주세요.',
        }
        
        self.fields['email'].error_messages = {
            'invalid': '올바른 이메일 주소를 입력해주세요.',
            'required': '이메일을 입력해주세요.',
        }

        self.fields['password1'].error_messages = {
            'required': '비밀번호를 입력해주세요.',
            'password_too_short': '비밀번호는 최소 8자 이상이어야 합니다.',
            'password_too_common': '너무 일반적인 비밀번호입니다.',
            'password_entirely_numeric': '비밀번호는 숫자로만 이루어질 수 없습니다.',
        }

        self.fields['password2'].error_messages = {
            'required': '비밀번호 확인을 입력해주세요.',
            'password_mismatch': '비밀번호가 일치하지 않습니다.',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': '사용자 이름',
            'email': '이메일',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'disabled': 'disabled'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'disabled': 'disabled'
            }),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'bio', 'favorite_wine', 'price_range']
        labels = {
            'profile_image': '프로필 이미지',
            'bio': '자기소개',
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '자기소개를 입력해주세요'
            }),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
            'placeholder': '이메일 주소'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
            'placeholder': '아이디'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
            'placeholder': '비밀번호'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
            'placeholder': '비밀번호 확인'
        })
    )

    # 약관 동의 필드들
    terms_service = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-purple-600'}),
        error_messages={'required': '서비스 이용약관에 동의해주세요.'}
    )
    terms_privacy = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-purple-600'}),
        error_messages={'required': '개인정보 처리방침에 동의해주세요.'}
    )
    terms_marketing = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-purple-600'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',
                  'terms_service', 'terms_privacy', 'terms_marketing')


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
            'placeholder': '가입시 등록한 이메일 주소'
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('해당 이메일로 등록된 계정이 없습니다.')
        return email