from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegisterForm, LoginForm, CommentForm
from .models import User, Dwarf, Comment, UserDwarf, UserAchievement, Achievement
from django.db.models import Count
import qrcode
from django.http import HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Dwarf
from django.contrib.auth.decorators import login_required
import json


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
    if request.user.is_authenticated:
        user_dwarfs = UserDwarf.objects.filter(user=request.user).values_list('dwarf_id', flat=True)
    return render(request, 'dwarfs.html', {'dwarfs': dwarfs, 'user_dwarfs': user_dwarfs})


def dwarf_detail_view(request, pk):
    dwarf = get_object_or_404(Dwarf, pk=pk)
    comments = Comment.objects.filter(dwarf=dwarf).order_by('-comment_date')
    has_unlocked = UserDwarf.objects.filter(user=request.user, dwarf=dwarf).exists()
    user_comments_count = 0
    if request.user.is_authenticated:
        user_comments_count = Comment.objects.filter(user=request.user, dwarf=dwarf).count()
    return render(request, 'dwarf_detail.html', {'dwarf': dwarf, 'comments': comments, 'has_unlocked': has_unlocked,
                                                 'user_comments_count': user_comments_count})


@login_required
def dwarf_comment_view(request, pk):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        dwarf = get_object_or_404(Dwarf, pk=pk)
        Comment.objects.create(user=request.user, dwarf=dwarf, comment_text=comment_text)
        return redirect('dwarf_detail', pk=pk)


@login_required
def dwarf_comment_create_view(request, pk):
    dwarf = get_object_or_404(Dwarf, pk=pk)
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
            return redirect('dwarf_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form, 'dwarf': dwarf})


@login_required
def dwarf_comment_delete_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        messages.error(request, "Nie masz uprawnień do usunięcia tego komentarza.")
        return redirect('dwarf_detail', pk=comment.dwarf.pk)
    comment.delete()
    messages.success(request, "Komentarz został usunięty.")
    return redirect('dwarf_detail', pk=comment.dwarf.pk)


@login_required
def users_ranking_view(request):
    users = User.objects.annotate(num_dwarfs=Count('userdwarf')).order_by('-num_dwarfs')
    return render(request, 'users_ranking.html', {'users': users})


@login_required
def user_achievements_view(request):
    user_achievements = UserAchievement.objects.filter(user=request.user)
    all_achievements = Achievement.objects.all()
    achievements_to_gain = all_achievements.exclude(id__in=user_achievements.values_list('achievement_id', flat=True))
    return render(request, 'user_achievements.html',
                  {'user_achievements': user_achievements, 'achievements_to_gain': achievements_to_gain})


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


@csrf_exempt
@login_required
def verify_qr_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        qr_code = data.get('qr_code')
        try:
            dwarf = Dwarf.objects.get(pk=qr_code.split('/')[-2])
            user_dwarf = UserDwarf.objects.filter(user=request.user, dwarf=dwarf).first()
            if user_dwarf:
                return JsonResponse({'success': False, 'message': 'Ten krasnal został już odblokowany.', 'url': reverse('dwarf_detail', args=[dwarf.id])})
            else:
                UserDwarf.objects.create(user=request.user, dwarf=dwarf)
                return JsonResponse({'success': True, 'url': reverse('dwarf_detail', args=[dwarf.id])})
        except Dwarf.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Nieprawidłowy kod QR.'})
    else:
        return JsonResponse({'success': False, 'message': 'Nieprawidłowe żądanie.'})
