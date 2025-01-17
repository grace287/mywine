from django.db import models
from django.conf import settings

# WineCountry 모델을 먼저 정의
class WineCountry(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='국가명(영문)')
    name_kr = models.CharField(max_length=100, verbose_name='국가명(한글)')
    is_common = models.BooleanField(default=False, verbose_name='주요 생산국')

    class Meta:
        verbose_name = '와인 생산국'
        verbose_name_plural = '와인 생산국 관리'
        ordering = ['-is_common', 'name_kr']

    def __str__(self):
        return self.name_kr


WINE_TYPES = [
        ('red', '레드'),
        ('white', '화이트'),
        ('sparkling', '스파클링'),
        ('rose', '로제'),
        ('champagne', '샴페인'),
        ('dessert', '디저트 와인'),
        ('fortified', '주정강화 와인'),
        ('orange', '오렌지와인'),
        ('natural', '내추럴 와인'),
        ('other', '기타'),
    ]

WINE_COLORS = [
        ('purple', 'Purple'),
        ('ruby', 'Ruby'),
        ('garnet', 'Garnet'),
        ('tawny', 'Tawny'),
        ('brown', 'Brown'),
        ('deep_red', 'Deep Red'),

        # 화이트
        ('lemon', 'Lemon'),
        ('gold', 'Gold'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),

        # 로제
        ('pink', 'Pink'),
        ('apricot', 'Apricot'),
        ('strawberry', 'Strawberry'),
        ('coral', 'Coral'),

        # 샴페인
        ('gold', 'Gold'),

        # 기타
        ('white', 'White'),
        ('orange', 'Orange'),

    ]

WINE_PRODUCING_COUNTRIES = [
        ("France", "프랑스"),
        ("Italy", "이탈리아"),
        ("USA", "미국"),
        ("Spain", "스페인"),
        ("Argentina", "아르헨티나"),
        ("Australia", "호주"),
        ("Chile", "칠레"),
        ("South Africa", "South Africa"),
        ("Germany", "Germany"),
        ("Portugal", "Portugal"),
        ("New Zealand", "New Zealand"),
        ("Austria", "Austria"),
        ("Hungary", "Hungary"),
        ("Greece", "Greece"),
        ("Canada", "Canada"),
        ("Japan", "Japan"),
        ("South Korea", "South Korea"),
        ("Brazil", "Brazil"),
        ("China", "China"),
        ("Switzerland", "Switzerland"),
        ("Other", "Other"),
    ]

AROMA_TYPES = [
    # 과일
    ('apple', '사과'),
    ('pear', '배'),
    ('peach', '복숭아'),
    ('plum', '자두'),
    ('cherry', '체리'),
    ('berry', '베리'),
    ('citrus', '시트러스'),
    ('stone_fruit', '과육'),
    ('tropical_fruit', '열대과일'),
    ('pineapple', '파인애플'),
    ('banana', '바나나'),
    ('mango', '망고'),
    ('papaya', '파파야'),
    
    # floral
    ('rose', '장미'),
    ('lilac', '라일락'),
    ('violet', '바이올렛'),
    ('iris', '아이리스'),
    ('jasmine', '자스민'),
    ('lavender', '라벤더'),
    ('peony', '포아니'),
    ('daisy', '데이지'),    

    # 향신료
    ('vanilla', '바닐라'),
    ('coffee', '커피'),
    ('chocolate', '초콜릿'),
    ('herbal', '허브'),
    ('herb', '허브'),

    # 나무향
    ('oak', '오크'),
    ('cedar', '세이드'),
    ('vanilla', '바닐라'),
    ('coffee', '커피'),
    ('chocolate', '초콜릿'),
    ('herbal', '허브'),
    
    # 견과류
    ('almond', '아몬드'),
    ('peanut', '땅콩'),
    ('walnut', '호두'),
    ('hazelnut', '헤이즐넛'),
    ('pecan', '페칸'),
    ('pistachio', '피스타치오'), 

    # 기타
    ('leather', '가죽'),
    ('chocolate', '초콜릿'),
  
]

class TastingNote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes_tasting_notes") # Changed
    
    # 기본 와인 정보
    wine_name = models.CharField(max_length=100, verbose_name="와인 이름")
    wine_type = models.CharField(max_length=20, choices=WINE_TYPES, verbose_name="와인 종류")
    grape_varieties = models.CharField(max_length=200, blank=True, null=True, verbose_name="포도 품종")
    vintage = models.IntegerField(blank=True, null=True, verbose_name="빈티지")
    country = models.ForeignKey(
        WineCountry, 
        on_delete=models.PROTECT, 
        null=True,  # 임시로 null 허용
        blank=True,  # 임시로 blank 허용
        related_name='tasting_notes', 
        verbose_name='생산국'
    )
    winery = models.CharField(max_length=100, blank=True, null=True, verbose_name="와이너리") # 선택
    
    # 테이스팅 정보
    tasting_date = models.DateField(verbose_name="테이스팅 날짜")
    tasting_place = models.CharField(max_length=200, verbose_name="테이스팅 장소", default="Unknown")
    tasting_with = models.CharField(max_length=200, verbose_name="테이스팅 대상", default="Unknown")
    
    price = models.IntegerField(null=True, blank=True, verbose_name="가격")
    price_place = models.CharField(max_length=200, blank=True, null=True, verbose_name="구입처")

    # 외관 평가
    appearance_intensity = models.IntegerField(
        choices=[
        (1, '매우 연함'),
        (2, '연함'),
        (3, '보통'),
        (4, '진함'),
        (5, '매우 진함'),
    ], verbose_name='색의 강도', default=3)
    
    appearance_clarity = models.CharField(max_length=50, choices=[
        ('clear', '맑음'),
        ('hazy', '흐림'),
        ('cloudy', '탁함'),
    ], verbose_name='투명도', default='clear')

    appearance_color = models.CharField(max_length=50, choices=WINE_COLORS, verbose_name='색상', default='purple')
    
    # 아로마
    aroma_intensity = models.IntegerField(choices=[
        (1, '매우 약함'),
        (2, '약함'),
        (3, '중간'),
        (4, '강함'),
        (5, '매우 강함'),
    ], verbose_name='아로마 강도', default=3)
    aroma_type = models.CharField(max_length=50, choices=AROMA_TYPES, verbose_name='아로마 타입', default='apple')
    aroma_notes = models.TextField(blank=True, null=True, verbose_name="아로마 노트")
    
    # 맛
    taste_sweetness = models.IntegerField(choices=[
        (1, '매우 드라이'),
        (2, '드라이'),
        (3, '중간'),
        (4, '스위트'),
        (5, '매우 스위트'),
    ], verbose_name='당도', default=3)
    
    taste_acidity = models.IntegerField(choices=[
        (1, '매우 낮음'),
        (2, '낮음'),
        (3, '중간'),
        (4, '높음'),
        (5, '매우 높음'),
    ], verbose_name='산도', default=3)
    
    taste_tannin = models.IntegerField(choices=[
        (1, '매우 부드러움'),
        (2, '부드러움'),
        (3, '중간'),
        (4, '강함'),
        (5, '매우 강함'),
    ], verbose_name='탄닌', default=3)
    
    taste_body = models.IntegerField(choices=[
        (1, '매우 가벼움'),
        (2, '가벼움'),
        (3, '중간'),
        (4, '무거움'),
        (5, '매우 무거움'),
    ], verbose_name='바디', default=3)

    taste_notes = models.JSONField(default=list, verbose_name='맛 노트')


    # 종합 평가
    rating = models.IntegerField(
        choices=[
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ], verbose_name='평점', default=3)
    tasting_pairing = models.CharField(max_length=200, verbose_name="테이스팅 페어링", default="Unknown")
    
    overall = models.TextField(verbose_name='종합 평가')
    is_public = models.BooleanField(default=False, verbose_name="공개 여부")
    
    # 이미지
    image = models.ImageField(upload_to='tasting_notes/', blank=True, null=True, verbose_name="이미지")

    # JSON 필드들
    aroma_notes = models.JSONField(default=list)
    taste_notes = models.JSONField(default=list)
    
    # 메타 데이터
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'notes'
        ordering = ['-created_at']
        verbose_name = '테이스팅 노트'
        verbose_name_plural = '테이스팅 노트들'
    
    def __str__(self):
        return f"{self.wine_name} ({self.tasting_date})"
    




class Event(models.Model):
    title = models.CharField(max_length=200)  # 제목 필드 추가
    start_date = models.DateField()  # 시작 날짜 필드 추가
    end_date = models.DateField()  # 종료 날짜 필드 추가
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events"
    )  # 사용자와 연결

    def __str__(self):
        return self.title

class TastingEvent(models.Model):
    tasting_note = models.ForeignKey(
        'TastingNote',
        on_delete=models.CASCADE,
        related_name='tasting_events'
    )
    date = models.DateField(verbose_name="테이스팅 날짜")  # date 필드 추가

    def __str__(self):
        return f"Tasting Event for {self.tasting_note} on {self.date}"


class Wine(models.Model):
    name = models.CharField(max_length=200, verbose_name='와인 이름')
    winery = models.CharField(max_length=200, verbose_name='와이너리')
    vintage = models.CharField(max_length=4, blank=True, verbose_name='빈티지')
    wine_type = models.CharField(
        max_length=50, 
        choices=WINE_TYPES, 
        verbose_name='와인 종류'
    )
    region = models.CharField(max_length=200, verbose_name='생산지역')
    grapes = models.JSONField(default=list, verbose_name='포도 품종')  # 포도 품종 목록
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['winery']),
        ]
        verbose_name = '와인'
        verbose_name_plural = '와인들'
    
    def __str__(self):
        return f"{self.name} ({self.vintage}) - {self.winery}"

    def get_grapes_display(self):
        """포도 품종 목록을 문자열로 반환"""
        return ', '.join(self.grapes)