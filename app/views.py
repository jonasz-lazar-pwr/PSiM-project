import json
import qrcode

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import CommentForm, LoginForm, RegisterForm
from .models import Achievement, Comment, Dwarf, User, UserAchievement, UserDwarf


def home_view(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = LoginForm()
    return render(request=request, template_name="login.html", context={"form": form})


def dwarfs_list_view(request):
    query = request.GET.get('q', '')
    dwarfs = Dwarf.objects.filter(name__icontains=query).order_by('name')
    user_dwarfs = []
    total_dwarfs = Dwarf.objects.count()
    user_dwarfs_count = 0
    if request.user.is_authenticated:
        user_dwarfs = UserDwarf.objects.filter(user=request.user).values_list('dwarf_id', flat=True)
        user_dwarfs_count = UserDwarf.objects.filter(user=request.user).count()
    return render(request, 'dwarfs.html', {'dwarfs': dwarfs, 'user_dwarfs': user_dwarfs, 'total_dwarfs': total_dwarfs,
                                           'user_dwarfs_count': user_dwarfs_count})


def dwarf_detail_view(request, pk):
    dwarf = get_object_or_404(Dwarf, pk=pk)
    comments = Comment.objects.filter(dwarf=dwarf).order_by('-comment_date')
    has_unlocked = False
    user_comments_count = 0
    if request.user.is_authenticated:
        has_unlocked = UserDwarf.objects.filter(user=request.user, dwarf=dwarf).exists()
        user_comments_count = Comment.objects.filter(user=request.user, dwarf=dwarf).count()
    context = {
        'dwarf': dwarf,
        'comments': comments,
        'has_unlocked': has_unlocked,
        'user_comments_count': user_comments_count,
    }
    return render(request, 'dwarf_detail.html', context)


@login_required
def dwarf_comment_create_view(request, pk):
    dwarf = get_object_or_404(Dwarf, pk=pk)
    has_unlocked = UserDwarf.objects.filter(user=request.user, dwarf=dwarf).exists()
    if not has_unlocked:
        messages.error(request, "Nie możesz dodać komentarza do krasnala, którego jeszcze nie odblokowałeś.")
        return redirect('dwarf_detail', pk=pk)
    user_comments_count = Comment.objects.filter(user=request.user, dwarf=dwarf).count()
    if user_comments_count >= 3:
        messages.error(request, "Dodano maksymalną liczbę komentarzy dla tego krasnala.")
        return redirect('dwarf_detail', pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.dwarf = dwarf
            comment.save()
            check_and_assign_comment_achievements(request.user)
            return redirect('dwarf_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form, 'dwarf': dwarf})


def check_and_assign_comment_achievements(user):
    user_comments_count = Comment.objects.filter(user=user).count()
    all_achievements = Achievement.objects.filter(comment_count__gt=0)

    # Assign new achievements
    for achievement in all_achievements:
        if user_comments_count >= achievement.comment_count:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user, achievement=achievement)
            if created:
                pass

    # Remove achievements if the user no longer qualifies for them
    user_achievements = UserAchievement.objects.filter(user=user)
    for user_achievement in user_achievements:
        if user_comments_count < user_achievement.achievement.comment_count:
            user_achievement.delete()


@login_required
def dwarf_comment_view(request, pk):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        dwarf = get_object_or_404(Dwarf, pk=pk)
        Comment.objects.create(user=request.user, dwarf=dwarf, comment_text=comment_text)
        check_and_assign_comment_achievements(request.user)
        return redirect('dwarf_detail', pk=pk)


@login_required
def dwarf_comment_delete_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        messages.error(request, "Nie masz uprawnień do usunięcia tego komentarza.")
        return redirect('dwarf_detail', pk=comment.dwarf.pk)
    comment.delete()
    check_and_assign_comment_achievements(request.user)
    messages.success(request, "Komentarz został usunięty.")
    return redirect('dwarf_detail', pk=comment.dwarf.pk)


@login_required
def users_ranking_view(request):
    sort_by = request.GET.get('sort_by', 'num_dwarfs')
    users = User.objects.annotate(
        num_dwarfs=Count('userdwarf', distinct=True),
        num_comments=Count('comment', distinct=True)
    ).order_by('-' + sort_by)
    return render(request, 'users_ranking.html', {'users': users})


@login_required
def user_achievements_view(request):
    user_achievements = UserAchievement.objects.filter(user=request.user).order_by('-achievement_date')
    all_achievements = Achievement.objects.all()
    achievements_to_gain = all_achievements.exclude(id__in=user_achievements.values_list('achievement_id', flat=True))
    return render(request, 'user_achievements.html',
                  {'user_achievements': user_achievements, 'achievements_to_gain': achievements_to_gain})


@login_required
def user_comments_view(request):
    user_comments = Comment.objects.filter(user=request.user).order_by('-comment_date')
    return render(request, 'user_comments.html', {'user_comments': user_comments})


def generate_qr_code(request, pk):
    dwarf = get_object_or_404(Dwarf, pk=pk)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    url = request.build_absolute_uri(reverse('dwarf_detail', kwargs={'pk': dwarf.pk}))
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


@login_required
def scan_qr_code(request):
    return render(request, 'scan_qr_code.html')


def check_and_assign_achievements(user):
    user_dwarfs_count = UserDwarf.objects.filter(user=user).count()
    all_achievements = Achievement.objects.filter(dwarf_count__gt=0)

    for achievement in all_achievements:
        if user_dwarfs_count >= achievement.dwarf_count:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user, achievement=achievement)
            if created:
                pass


@login_required
@csrf_exempt
def verify_qr_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        qr_code = data.get('qr_code')
        try:
            dwarf = Dwarf.objects.get(pk=qr_code.split('/')[-2])
            user_dwarf, created = UserDwarf.objects.get_or_create(user=request.user, dwarf=dwarf)
            if created:
                check_and_assign_achievements(request.user)
                return JsonResponse({'success': True, 'url': reverse('dwarf_detail', args=[dwarf.id])})
            else:
                return JsonResponse({'success': False, 'message': 'Ten krasnal został już odblokowany.',
                                     'url': reverse('dwarf_detail', args=[dwarf.id])})
        except Dwarf.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Nieprawidłowy kod QR.'})
    else:
        return JsonResponse({'success': False, 'message': 'Nieprawidłowe żądanie.'})
