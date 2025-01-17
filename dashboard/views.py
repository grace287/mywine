import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from notes.models import TastingNote  # notes 앱의 TastingNote 모델 import
from django.db.models.functions import TruncMonth  # TruncMonth import 추가
from django.utils import timezone
from django.db.models import Count, F, Sum, Case, When, Value, CharField, Avg
from datetime import timedelta
from datetime import datetime, timedelta
from django.db.models import Case, When, Value, CharField
import calendar


@login_required(login_url='/users/login/')
def filter_results(request):
    wine_type_filter = request.GET.get('wine_type', '')
    country_filter = request.GET.get('country', '')
    notes = TastingNote.objects.filter(user=request.user)
    if wine_type_filter:
        notes = notes.filter(wine_type=wine_type_filter)
    if country_filter:
        notes = notes.filter(country=country_filter)

    paginator = Paginator(notes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/filter_results.html', {
        'page_obj': page_obj,
        'wine_type_filter': wine_type_filter,
        'country_filter': country_filter
    })


@login_required
def statistics(request):
    total_notes = TastingNote.objects.filter(user=request.user)
    total_notes_count = total_notes.count()
    
    # 통계 카드 데이터
    statistics_cards = [
        {
            'label': '총 시음 횟수',
            'value': total_notes_count,
            'icon': 'fas fa-wine-glass-alt',
            'change': 12.5  # 전월 대비 증가율
        },
        {
            'label': '평균 평점',
            'value': total_notes.aggregate(Avg('rating'))['rating__avg'] or 0,
            'icon': 'fas fa-star',
            'change': 5.2
        },
        {
            'label': '평균 가격',
            'value': total_notes.aggregate(Avg('price'))['price__avg'] or 0,
            'icon': 'fas fa-tag',
            'change': -3.8
        },
        {
            'label': '가장 선호하는 와인',
            'value': '레드',  # 예시 데이터
            'icon': 'fas fa-heart',
            'change': 0
        }
    ]
    
    # 맛 프로필 평균
    taste_profile = {
        'sweetness': 2.8,
        'acidity': 3.5,
        'tannin': 3.2,
        'body': 3.8
    }
    
    # 와인 타입 분포
    wine_type_counts = [
        {'type': 'Red', 'count': 45},
        {'type': 'White', 'count': 30},
        {'type': 'Sparkling', 'count': 15},
        {'type': 'Rosé', 'count': 10}
    ]
    
    # 지역별 분포
    region_counts = [
        {'country': 'France', 'count': 25},
        {'country': 'Italy', 'count': 20},
        {'country': 'Spain', 'count': 15},
        {'country': 'USA', 'count': 12},
        {'country': 'Chile', 'count': 8}
    ]
    
    context = {
        'total_notes_count': total_notes_count,
        'statistics_cards': statistics_cards,
        'taste_profile': json.dumps(taste_profile),
        'wine_type_counts': json.dumps(wine_type_counts),
        'region_counts': json.dumps(region_counts)
    }
    
    return render(request, 'dashboard/statistics.html', context)


def wine_statistics_view(request):
    user = request.user
    total_notes = TastingNote.objects.filter(user=user).count()
    average_rating = TastingNote.objects.filter(user=user).aggregate(Avg('rating'))['rating__avg']
    favorite_wine = TastingNote.objects.filter(user=user).order_by('-rating').first()
    
    # 선호하는 와인 타입 및 아로마 향 계산
    preferred_wine_type = TastingNote.objects.filter(user=user).values('wine_type').annotate(count=Count('id')).order_by('-count').first()
    preferred_aroma = TastingNote.objects.filter(user=user).values('aroma').annotate(count=Count('id')).order_by('-count').first()

    return render(request, 'notes/wine_statistics.html', {
        'total_notes': total_notes,
        'average_rating': average_rating,
        'favorite_wine': favorite_wine.wine_name if favorite_wine else "데이터 없음",
        'preferred_wine_type': preferred_wine_type['wine_type'] if preferred_wine_type else "데이터 없음",
        'preferred_aroma': preferred_aroma['aroma'] if preferred_aroma else "데이터 없음",
    })