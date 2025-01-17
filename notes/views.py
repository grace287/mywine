import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, F, Avg
from django.core.paginator import Paginator
from .models import TastingNote, TastingEvent, WineCountry
from .forms import TastingNoteForm
from django.utils import timezone
import calendar
from django.urls import reverse
from django.http import JsonResponse
from taggit.models import Tag  # Tag를 notes.models 대신 taggit에서 import
from datetime import date, timedelta
from django.http import HttpResponseBadRequest
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Event
import logging
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import datetime
from .models import Wine
import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.safestring import mark_safe
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt  # CSRF 예외 처리가 필요한 경우
from django.core.cache import cache
from django.http import HttpResponseBadRequest

logger = logging.getLogger(__name__)


def get_events(request):
       if not request.user.is_authenticated:
           return JsonResponse([], safe=False)

       start = request.GET.get('start')
       end = request.GET.get('end')

       try:
           events = Event.objects.filter(
               user=request.user,
               start_date__range=(start, end),
           ).values('title', 'start_date', 'end_date')

           events_list = [
               {
                   "title": event['title'],
                   "start": event['start_date'],
                   "end": event.get('end_date', None),
               }
               for event in events
           ]
           return JsonResponse(events_list, safe=False)
       except Exception as e:
           return JsonResponse({'error': str(e)}, status=500)
       
def calendar_view(request):
    # GET 요청일 때는 템플릿 렌더링
    if request.method == 'GET':
        notes = TastingNote.objects.filter(user=request.user).order_by('-tasting_date')
        
        # 캘린더 이벤트용 데이터 생성
        events = []
        for note in notes:
            event = {
                'id': note.id,
                'title': note.wine_name,
                'start': note.tasting_date.strftime('%Y-%m-%d'),  # 날짜 포맷 변환
                'url': f'/notes/{note.id}/',  # 노트 상세 페이지 URL
                'backgroundColor': get_wine_color(note),  # 와인 종류에 따른 색상
            }
            events.append(event)
        
        context = {
            'notes': notes,
            'events_json': json.dumps(events, cls=DjangoJSONEncoder)  # JSON으로 변환
        }
        
        return render(request, 'notes/calendar.html', context)
    
    # AJAX 요청 처리 (달력 이벤트 데이터)
    notes = TastingNote.objects.filter(user=request.user)
    events = []
    for note in notes:
        event = {
            'id': note.id,
            'title': note.wine_name,
            'start': note.tasting_date.strftime('%Y-%m-%d'),
            'url': f'/notes/{note.id}/',
            'backgroundColor': get_wine_color(note),
        }
        events.append(event)
    
    return JsonResponse(events, safe=False)

def get_wine_color(note):
    """와인 종류에 따른 색상 반환"""
    wine_colors = {
        'red': '#dc2626',     # 레드 와인
        'white': '#fbbf24',   # 화이트 와인
        'rose': '#f472b6',    # 로제 와인
        'sparkling': '#60a5fa',  # 스파클링
        'fortified': '#7c3aed',  # 주정강화
        'dessert': '#c084fc',    # 디저트
    }
    return wine_colors.get(note.wine_type, '#6b7280')  # 기본값은 회색

@login_required
def home(request, year=None, month=None):
    notes = TastingNote.objects.all()  # 모든 노트 가져오기
    # 년도와 월이 지정되지 않은 경우 현재 날짜 사용
    if year is None or month is None:
        now = timezone.now()
        year = now.year
        month = now.month

    # 해당 월의 시음노트 가져오기
    notes = TastingNote.objects.filter(
        user=request.user,
        tasting_date__year=year,
        tasting_date__month=month
    ).order_by('-tasting_date')
    # 최근 시음노트 가져오기
    recent_notes = TastingNote.objects.filter(user=request.user).order_by('-tasting_date')[:5]
    
    # 노트 개수 집계
    note_counts = (
        TastingNote.objects
        .filter(user=request.user)
        .values('tasting_date')
        .annotate(count=Count('id'))
    )
    
    calendar_data = {note['tasting_date'].strftime('%Y-%m-%d'): note['count'] for note in note_counts}

    context = {
        'year': year,
        'month': month,
        'notes': notes,
        'recent_notes': recent_notes,  # 최근 시음노트
        'note_counts': json.dumps(calendar_data),  # 캘린더 데이터
    }
    return render(request, 'notes/calendar.html', context)


@login_required(login_url='/users/login/') # login_url 변경
def note_detail(request, note_id):
    try:
        note = get_object_or_404(TastingNote, id=note_id, user=request.user)
        return JsonResponse({
            'wine_name': note.wine_name,
            'winery': note.winery,
            'wine_type': note.wine_type,
            'vintage': note.vintage,
            'price': note.price,
            'tasting_date': note.tasting_date,
            'appearance_intensity': note.appearance_intensity,
            'appearance_clarity': note.appearance_clarity,
            'aroma_intensity': note.aroma_intensity,

            'overall': note.overall,
            'sweetness': note.sweetness,
            'acidity': note.acidity,
            'tannin': note.tannin,
            'body': note.body,
            'taste_notes': note.taste_notes,

        })
    except Http404:
        return JsonResponse({'error': '노트를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        logger.error(f"Error in note_detail: {e}")
        return JsonResponse({'error': '서버 오류가 발생했습니다.'}, status=500)

@require_http_methods(["POST"])
@login_required
def note_create(request):
    if request.method == 'POST':
        # 기본값을 설정하고 POST 데이터에서 가져오기
        appearance_intensity = request.POST.get('appearance_intensity', 3)
        appearance_clarity = request.POST.get('appearance_clarity', 3)
        aroma_intensity = request.POST.get('aroma_intensity', 3)
        sweetness = request.POST.get('sweetness', 3)
        acidity = request.POST.get('acidity', 3)
        tannin = request.POST.get('tannin', 3)
        body = request.POST.get('body', 3)

        try:
            # 빈 문자열을 정수로 변환하기 전에 확인
            appearance_intensity = int(appearance_intensity) if appearance_intensity else 3
            aroma_intensity = int(aroma_intensity) if aroma_intensity else 3
            sweetness = int(sweetness) if sweetness else 3
            acidity = int(acidity) if acidity else 3
            tannin = int(tannin) if tannin else 3
            body = int(body) if body else 3

            # 폼 데이터 검증 및 저장
            form = TastingNoteForm(request.POST, request.FILES)
            if form.is_valid():
                # 폼 데이터에서 TastingNote 객체 생성
                note = form.save(commit=False)
                note.user = request.user
                note.appearance_intensity = appearance_intensity
                note.appearance_clarity = appearance_clarity
                note.aroma_intensity = aroma_intensity
                note.sweetness = sweetness
                note.acidity = acidity
                note.tannin = tannin
                note.body = body
                note.taste_notes = request.POST.get('taste_notes', '')
                note.save()

                # 최초 작성 여부 확인
                is_first_note = TastingNote.objects.filter(user=request.user).count() == 1
                return JsonResponse({
                    'success': True,
                    'message': '시음 노트가 성공적으로 저장되었습니다.',
                    'hide_example_section': is_first_note,
                    'redirect_url': reverse('notes:note_detail', args=[note.id])
                })

            # 폼이 유효하지 않은 경우
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        except Exception as e:
            # 예외 발생 처리
            logger.exception(f"Error creating tasting note: {e}")
            return JsonResponse({'success': False, 'error': '시음 노트 생성 중 오류가 발생했습니다.'}, status=500)


@login_required(login_url='/users/login/') # login_url 변경
def note_edit(request, note_id):
    note = get_object_or_404(TastingNote, pk=note_id, user=request.user)
    if request.method == 'POST':
        form = TastingNoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:note_detail', note_id=note.id)
    else:
        form = TastingNoteForm(instance=note)
    return render(request, 'notes/note_detail.html', {'form': form})


@login_required(login_url='/users/login/') # login_url 변경
def note_delete(request, note_id):
    note = get_object_or_404(TastingNote, pk=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('notes:gallery')
    return render(request, 'notes/note_delete.html', {'note': note})

@login_required
def note_detail(request, note_id):
    try:
        note = get_object_or_404(TastingNote, id=note_id, user=request.user)
        return JsonResponse({
            'wine_name': note.wine_name,
            'winery': note.winery,
            'vintage': note.vintage,
            'tasting_date': note.tasting_date,
            'overall': note.overall,
            'sweetness': note.sweetness,
            'acidity': note.acidity,
            'tannin': note.tannin,
            'body': note.body,
        })
    except Http404:
        return JsonResponse({'error': '노트를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        logger.error(f"Error in note_detail: {e}")
        return JsonResponse({'error': '서버 오류가 발생했습니다.'}, status=500)


@login_required(login_url='/users/login/') # login_url 변경
def search_notes(request):
    query = request.GET.get('q', '')  # 검색어를 가져옴
    notes = TastingNote.objects.filter(user=request.user)  # 현재 사용자의 모든 노트 가져옴
    if query:
        notes = notes.filter(
            Q(wine_name__icontains=query) |  # 와인 이름
            Q(wine_varietal__icontains=query) |  # 품종
            Q(winery__icontains=query) |  # 와이너리
            Q(tasting_place__icontains=query) |  # 테이스팅 장소
            Q(aroma_notes__icontains=query) |  # 아로마 노트
            Q(overall__icontains=query)  # 전체 평가
        )

        # 페이지네이션
        paginator = Paginator(notes, 5)  # 한 페이지에 5개씩
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    else:
        # 페이지네이션
        paginator = Paginator(notes, 5)  # 한 페이지에 5개씩
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, 'notes/search_results.html', {'page_obj': page_obj, 'query': query})

@login_required
def get_note_counts(request):
    notes = TastingNote.objects.filter(user=request.user)
    counts = {}
    for note in notes:
        date = str(note.tasting_date)
        counts[date] = counts.get(date, 0) + 1
    return JsonResponse(counts)


def get_note_detail(request, note_id):
    try:
        note = TastingNote.objects.get(id=note_id)
        data = {
            'wine_name': note.wine_name,
            'taste_notes': note.taste_notes,
            # 필요한 다른 필드들...
        }
        return JsonResponse(data)
    except TastingNote.DoesNotExist:
        return JsonResponse({'error': '노트를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        logger.exception(f"Error fetching note detail: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    

@login_required
def note_detail_api(request, note_id):
    try:
        note = get_object_or_404(TastingNote, id=note_id, user=request.user)
        # data = model_to_dict(note)
        note = TastingNote.objects.get(id=note_id)
        
        data = {
            'id': note.id,
            'wine_name': note.wine_name,
            'wine_type': note.wine_type,
            'vintage': note.vintage,
            'country': note.country,
            'winery': note.winery,
            'grape_varieties': note.grape_varieties,
            'price': note.price,
            'aroma_notes': note.aroma_notes,
            'overall': note.overall,
        }
        
        return JsonResponse(data)
    except TastingNote.DoesNotExist:
        return JsonResponse({'error': '노트를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        logger.exception(f"Error fetching note detail: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def notes_by_date(request, date):
    try:
        # 날짜 문자열을 datetime 객체로 변환
        target_date = datetime.strptime(date, '%Y-%m-%d').date()
        
        # 해당 날짜의 노트들 가져오기
        notes = TastingNote.objects.filter(
            user=request.user,
            tasting_date=target_date
        ).order_by('-created_at')

        notes_data = [{
            'id': note.id,
            'wine_name': note.wine_name,
            'winery': note.winery,
            'wine_type': note.wine_type,
            'wine_type_display': note.get_wine_type_display(),
            'rating': note.rating,
        } for note in notes]
        
        context = {
            'notes': notes,
            'target_date': target_date,
        }

        return JsonResponse({
            'date': date,
            'notes': notes_data
        })
        
        return render(request, 'notes/notes_by_date.html', context)
    except ValueError:
        messages.error(request, '잘못된 날짜 형식입니다.')
        return redirect('notes:home_default')
    
@login_required
def notes_by_date_api(request, date_str):
    try:
        # 날짜 문자열을 datetime 객체로 변환
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # 해당 날짜의 노트 조회
        notes = TastingNote.objects.filter(
            user=request.user,
            tasting_date=date_obj
        ).order_by('-created_at')
        
        # 노트 데이터 직렬화
        data = []
        for note in notes:
            note_data = {
                'id': note.id,
                'wine_name': note.wine_name,
                'wine_type': note.wine_type,
                'wine_type_display': note.get_wine_type_display() if note.wine_type else '-',
                'rating': note.rating if note.rating is not None else 0,
                'sweetness': note.taste_sweetness if note.taste_sweetness is not None else 0,
                'acidity': note.taste_acidity if note.taste_acidity is not None else 0,
                'tannin': note.taste_tannin if note.taste_tannin is not None else 0,
                'body': note.taste_body if note.taste_body is not None else 0,
            }
            data.append(note_data)
        
        # 디버깅을 위한 로그
        print(f"Date: {date_str}, Notes found: {len(data)}")
        
        return JsonResponse(data, safe=False)
        
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return JsonResponse({'error': '잘못된 날짜 형식입니다.'}, status=400)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='/users/login/') # login_url 변경
def filter_notes(request):
    wine_type_filter = request.GET.get('wine_type', '')
    country_filter = request.GET.get('country', '')
    notes = TastingNote.objects.filter(user=request.user)  # 모든 노트 가져오기
    if wine_type_filter:
        notes = notes.filter(wine_type=wine_type_filter)
    if country_filter:
        notes = notes.filter(country=country_filter)

    # 페이지네이션
    paginator = Paginator(notes, 5)  # 한 페이지에 5개씩
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'notes/filter_results.html', {'page_obj': page_obj, 'wine_type_filter': wine_type_filter,
                                                        'country_filter': country_filter})


def search_wines(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # 캐시 키 생성
    cache_key = f'wine_search_{query}'
    cached_results = cache.get(cache_key)
    if cached_results:
        return JsonResponse(cached_results, safe=False)
    
    try:
        # Vivino API 엔드포인트
        url = "https://api.vivino.com/v2/search/wines"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Accept-Language": "ko-KR,ko;q=0.9",
            "X-Requested-With": "XMLHttpRequest",
        }
        params = {
            "q": query,
            "per_page": 10,
            "language": "ko"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # 검색 결과 파싱
        wines = []
        for wine in data.get('matches', []):
            wine_data = {
                'id': wine.get('id'),
                'name': wine.get('name'),
                'winery': wine.get('winery', {}).get('name', ''),
                'vintage_year': wine.get('vintage', {}).get('year'),
                'wine_type': wine.get('type_id'),
                'country': wine.get('region', {}).get('country', {}).get('name', ''),
                'grape_varieties': ', '.join([g.get('name', '') for g in wine.get('grape_varieties', [])]),
                'image_url': wine.get('image', {}).get('location'),
                'price': None,  # Vivino API에서 가격 정보는 별도로 요청해야 함
                'rating': wine.get('statistics', {}).get('ratings_average'),
            }
            wines.append(wine_data)
        
        # 결과 캐싱 (1시간)
        cache.set(cache_key, wines, 3600)
        
        return JsonResponse(wines, safe=False)
        
    except requests.RequestException as e:
        logger.error(f"Vivino API 요청 오류: {str(e)}")
        return JsonResponse({
            'error': '와인 검색 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
        }, status=500)

def test_wine_api(request):
    try:
        # Vivino API 엔드포인트
        api_url = 'https://api.vivino.com/api/v2/search/wines'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        params = {
            'q': 'cabernet',  # 검색어
            'size': 5  # 결과 수
        }
        
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        
        wines = response.json()
        
        # 응답 데이터 가공
        formatted_wines = [{
            'name': wine.get('name', ''),
            'winery': wine.get('winery', {}).get('name', ''),
            'vintage': wine.get('vintage', {}).get('year', ''),
            'region': wine.get('region', {}).get('name', ''),
            'type': wine.get('type', {}).get('name', ''),
            'image_url': wine.get('image', {}).get('location', ''),
            'rating': wine.get('statistics', {}).get('ratings_average', 0),
        } for wine in wines.get('matches', [])]
        
        return JsonResponse({
            'success': True,
            'data': formatted_wines,
            'status': response.status_code
        })
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'status': getattr(e.response, 'status_code', 500)
        })



@login_required
def note_delete(request, note_id):
    note = get_object_or_404(TastingNote, id=note_id, user=request.user)
    note.delete()
    return redirect('notes:calendar')

@login_required
def wine_collection(request):
    # 기본 쿼리셋
    notes = TastingNote.objects.filter(user=request.user)
    
    # 필터 파라미터 가져오기
    wine_type = request.GET.get('wine_type')
    price_range = request.GET.get('price')
    rating = request.GET.get('rating')
    grape_varieties = request.GET.get('grape_varieties')
    sort_by = request.GET.get('sort', '-created_at')  # 기본값: 최신순
    
    # 필터 적용
    if wine_type:
        notes = notes.filter(wine_type=wine_type)
    if grape_varieties:
        notes = notes.filter(grape_varieties=grape_varieties)
    if price_range:
        min_price, max_price = map(int, price_range.split('-'))
        notes = notes.filter(price__gte=min_price, price__lte=max_price)
    if rating:
        notes = notes.filter(rating=rating)
        
    # 정렬 적용
    notes = notes.order_by(sort_by)
    
    # 집계 데이터
    aggregates = {
        'total_count': notes.count(),
        'avg_rating': notes.aggregate(Avg('rating'))['rating__avg'],
        'avg_price': notes.aggregate(Avg('price'))['price__avg'],
    }
    
    # 필터 옵션 데이터
    filter_options = {
        'countries': notes.values('country').annotate(count=Count('id')).order_by('-count'),
        'wine_types': notes.values('wine_type').annotate(count=Count('id')).order_by('-count'),
        'price_ranges': [
            {'range': '0-30000', 'label': '3만원 이하'},
            {'range': '30000-50000', 'label': '3-5만원'},
            {'range': '50000-100000', 'label': '5-10만원'},
            {'range': '100000-200000', 'label': '10-20만원'},
            {'range': '200000-999999999', 'label': '20만원 이상'},
        ],
        'ratings': range(1, 6),
    }
    
    # 페이지네이션
    paginator = Paginator(notes, 12)  # 페이지당 12개
    page = request.GET.get('page', 1)
    notes = paginator.get_page(page)
    
    context = {
        'notes': notes,
        'aggregates': aggregates,
        'filter_options': filter_options,
        'current_filters': {
            'type': wine_type,
            'grape_varieties': grape_varieties,
            'price': price_range,
            'rating': rating,
            'sort': sort_by,
        },
    }
    
    return render(request, 'notes/collection.html', context)

@require_http_methods(["GET"])
def search_countries(request):
    query = request.GET.get('q', '')
    # 예시 데이터 - 실제로는 데이터베이스에서 검색
    countries = [
        {"id": 1, "name": "미국", "name_kr": "미국"},
        {"id": 2, "name": "France", "name_kr": "프랑스"},
        {"id": 3, "name": "Italy", "name_kr": "이탈리아"},
        # ... 더 많은 국가들
    ]
    
    filtered_countries = [
        country for country in countries 
        if query.lower() in country['name_kr'].lower() or query.lower() in country['name'].lower()
    ]
    
    return JsonResponse(filtered_countries, safe=False)
