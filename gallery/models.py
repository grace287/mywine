from django.db import models
from django.conf import settings
from notes.models import TastingNote

class Gallery(models.Model):
    tasting_note = models.ForeignKey(TastingNote, on_delete=models.CASCADE, related_name="gallery")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasting_notes")
    WINE_TYPES = [
        ('red', '레드'),
        ('white', '화이트'),
        ('sparkling', '샴페인'),
        ('rose', '로제'),
        ('fortified', '주정강화'),
        ('other', '기타'),
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
    wine_name = models.CharField(max_length=100, verbose_name="와인 이름")
    wine_type = models.CharField(max_length=20, choices=WINE_TYPES, verbose_name="와인 종류", default='red')  # 와인 종류
    wine_varietal = models.CharField(max_length=200, blank=True, null=True, verbose_name="와인 품종")  # 와인 품종
    country = models.CharField(
        max_length=100,
        verbose_name="국가",
        choices=WINE_PRODUCING_COUNTRIES,
        default="Other",
    )
    winery = models.CharField(max_length=100, blank=True, null=True, verbose_name="와이너리")
    vintage = models.IntegerField(
        choices=[(year, str(year)) for year in range(1800, 2025)],
        blank=True,
        null=True,
        verbose_name="빈티지"
    )
    tasting_date = models.DateField(verbose_name="테이스팅 날짜")
    tasting_place = models.CharField(max_length=200, verbose_name="테이스팅 장소", default="Unknown")
    # 외관 평가
    appearance_clarity = models.CharField(
        max_length=20,
        choices=[
            ("맑음", "맑음"),
            ("약간 탁함", "약간 탁함"),
            ("탁함", "탁함"),
            ("불투명", "불투명")
        ],
        verbose_name="투명도",
        default="맑음"
    )
    appearance_intensity = models.PositiveIntegerField(verbose_name="색의 강도", default=3)  # 슬라이더 (1~5)

    # 아로마
    aroma_intensity = models.PositiveIntegerField(verbose_name="향의 강도", default=3)  # 슬라이더 (1~5)
    aroma_notes = models.TextField(blank=True, null=True, verbose_name="아로마 노트")

    # 맛 평가
    sweetness = models.PositiveIntegerField(verbose_name="당도", default=3)  # 슬라이더 (1~5)
    acidity = models.PositiveIntegerField(verbose_name="산도", default=3)  # 슬라이더 (1~5)
    tannin = models.PositiveIntegerField(verbose_name="탄닌", default=3)  # 슬라이더 (1~5)
    body = models.PositiveIntegerField(verbose_name="바디", default=3)  # 슬라이더 (1~5)

    # 종합 평가
    overall = models.TextField(blank=True, null=True, verbose_name="종합 평가")

    is_public = models.BooleanField(default=False, verbose_name="공개 여부")
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="이미지")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.wine_name} ({self.vintage})"