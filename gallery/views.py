from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from notes.models import TastingNote  # Tag import 제거


@login_required(login_url='/users/login/')
def gallery_view(request):
    # 현재 선택된 뷰 타입
    current_view = request.GET.get('view', 'gallery')
    
    # 이미지가 있는 시음노트만 필터링
    notes = TastingNote.objects.filter(
        user=request.user,
        image__isnull=False
    ).order_by('-created_at')

    # 와인 타입으로 필터링
    wine_type = request.GET.get('type')
    if wine_type:
        notes = notes.filter(wine_type=wine_type)

    # 국가별 필터링
    country = request.GET.get('country')
    if country:
        notes = notes.filter(country__name=country)

    # 페이지네이션
    paginator = Paginator(notes, 12)  # 한 페이지당 12개 표시
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 필터링 옵션 준비
    wine_types = TastingNote.objects.filter(
        user=request.user,
        image__isnull=False
    ).values_list('wine_type', flat=True).distinct()
    
    countries = TastingNote.objects.filter(
        user=request.user,
        image__isnull=False
    ).values_list('country__name', flat=True).distinct()

    context = {
        'page_obj': page_obj,
        'wine_types': wine_types,
        'countries': countries,
        'current_view': current_view,
        'selected_type': wine_type,
        'selected_country': country,
    }

    return render(request, 'gallery/gallery.html', context)


@login_required(login_url='/users/login/') # login_url 변경
def gallery(request):
    notes = TastingNote.objects.filter(user=request.user).order_by('-created_at')

    # 페이지네이션
    paginator = Paginator(notes, 6)  # 한 페이지에 6개씩
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notes/gallery.html', {'page_obj': page_obj})