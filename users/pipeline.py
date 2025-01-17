from .models import Profile, UserProfile

def create_user_profile(backend, user, response, *args, **kwargs):
    """소셜 로그인 시 사용자 프로필을 생성하는 파이프라인"""
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)

    """소셜 로그인 시 사용자 프로필을 생성하는 파이프라인"""
    if backend.name == 'kakao':
        if not hasattr(user, 'profile'):
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': '',
                    'favorite_wine': '',
                    'price_range': ''
                }
            )
        
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'marketing_agreement': False
                }
            )

        return {'is_new': True}  # 새로운 사용자임을 표시
    
def get_naver_user_details(strategy, details, response, uid, user, *args, **kwargs):
    """
    네이버 사용자 정보를 처리하는 파이프라인
    """
    if not user:
        email = response.get('email')
        name = response.get('name')
        
        if email:
            user = strategy.create_user(
                email=email,
                username=email,
                first_name=name
            )
    
    return {
        'user': user,
        'is_new': user is None
    }