from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Post, Comment, Event, Tag, Notice
from .forms import PostForm, CommentForm, EventForm, NoticeForm
from notes.models import TastingNote
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def post_list(request):
    post_type = request.GET.get('type')
    search_query = request.GET.get('q')
    tag = request.GET.get('tag')
    
    # 기본 쿼리셋
    posts = Post.objects.select_related('user', 'tasting_note')  # author를 user로 변경
    
    # 필터링 적용
    if post_type:
        posts = posts.filter(post_type=post_type)
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    if tag:
        posts = posts.filter(tags__name=tag)
    
    # 정렬
    sort = request.GET.get('sort', 'recent')
    if sort == 'popular':
        posts = posts.order_by('-likes')
    elif sort == 'views':
        posts = posts.order_by('-views')
    else:  # recent
        posts = posts.order_by('-created_at')
    
    # 페이지네이션
    paginator = Paginator(posts, 10)  # 페이지당 10개 게시글
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'post_type': post_type,
        'search_query': search_query,
    }
    
    return render(request, 'community/post_list.html', context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related('author', 'tasting_note')
                            .prefetch_related('comments__author'), id=post_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('community:post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    
    # 조회수 증가
    post.views += 1
    post.save()
    
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'community/post_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '게시글이 작성되었습니다.')
            return redirect('community:post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'community/post_form.html', {'form': form})

@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # 작성자 확인
    if post.author != request.user:
        return HttpResponseForbidden("수정 권한이 없습니다.")
        
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, '게시글이 수정되었습니다.')
            return redirect('community:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'community/post_form.html', {
        'form': form,
        'post': post,
        'is_edit': True
    })

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # 작성자 확인
    if post.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")
        
    if request.method == 'POST':
        post.delete()
        messages.success(request, '게시글이 삭제되었습니다.')
        return redirect('community:post_list')
    
    return render(request, 'community/post_confirm_delete.html', {'post': post})

@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '댓글이 작성되었습니다.')
            return redirect('community:post_detail', post_id=post.id)
    
    return redirect('community:post_detail', post_id=post.id)

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # 작성자 확인
    if comment.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")
        
    if request.method == 'POST':
        post_id = comment.post.id
        comment.delete()
        messages.success(request, '댓글이 삭제되었습니다.')
        return redirect('community:post_detail', post_id=post_id)
    
    return render(request, 'community/comment_confirm_delete.html', {'comment': comment})

@login_required
def share_tasting_note(request, note_id):
    note = get_object_or_404(TastingNote, id=note_id, user=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.post_type = 'review'
            post.tasting_note = note
            post.save()
            messages.success(request, '시음노트가 공유되었습니다.')
            return redirect('community:post_detail', post_id=post.id)
    else:
        initial_data = {
            'title': f'{note.wine_name} 시음 후기',
            'content': f'와인: {note.wine_name}\n'
                      f'종류: {note.get_wine_type_display()}\n'
                      f'평점: {note.rating}/5\n\n'
                      f'테이스팅 노트:\n{note.overall}'
        }
        form = PostForm(initial=initial_data)
    
    return render(request, 'community/share_note.html', {
        'form': form,
        'note': note
    })

@login_required
def event_list(request):
    events = Event.objects.select_related('organizer').prefetch_related('participants')
    upcoming = events.filter(event_date__gte=timezone.now()).order_by('event_date')
    past = events.filter(event_date__lt=timezone.now()).order_by('-event_date')
    
    context = {
        'upcoming_events': upcoming,
        'past_events': past
    }
    return render(request, 'community/event_list.html', context)

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event.objects.select_related('organizer')
                             .prefetch_related('participants'), id=event_id)
    
    is_participant = request.user in event.participants.all()
    can_join = (not event.max_participants or 
                event.participants.count() < event.max_participants)
    
    if request.method == 'POST':
        if 'join' in request.POST and can_join and not is_participant:
            event.participants.add(request.user)
            messages.success(request, '이벤트 참가 신청이 완료되었습니다.')
        elif 'cancel' in request.POST and is_participant:
            event.participants.remove(request.user)
            messages.success(request, '이벤트 참가가 취소되었습니다.')
            
        return redirect('community:event_detail', event_id=event.id)
    
    context = {
        'event': event,
        'is_participant': is_participant,
        'can_join': can_join
    }
    return render(request, 'community/event_detail.html', context)

@login_required
def like_post(request, post_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            is_liked = False
        else:
            post.likes.add(request.user)
            is_liked = True

        return JsonResponse({
            'is_liked': is_liked,
            'likes_count': post.likes.count()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@staff_member_required
def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            return redirect('community:notice_list')
    else:
        form = NoticeForm()
    return render(request, 'community/notice_form.html', {'form': form})

def community_home(request):
    # 공지사항과 일반 게시글을 함께 표시
    notices = Notice.objects.all().order_by('-is_important', '-created_at')[:5]
    posts = Post.objects.all().order_by('-created_at')[:10]
    
    context = {
        'notices': notices,
        'posts': posts,
    }
    return render(request, 'community/home.html', context)

def notice_list(request):
    notices = Notice.objects.all().order_by('-is_important', '-created_at')
    return render(request, 'community/notice_list.html', {'notices': notices})

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.views += 1
    notice.save()
    return render(request, 'community/notice_detail.html', {'notice': notice})
