from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegisterForm, LoginForm, CommentForm
from .models import Dwarf, Comment, UserDwarf


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
    dwarfs = Dwarf.objects.all().order_by('name')
    return render(request, 'dwarfs.html', {'dwarfs': dwarfs})


def dwarf_detail_view(request, pk):
    dwarf = get_object_or_404(Dwarf, pk=pk)
    comments = Comment.objects.filter(dwarf=dwarf).order_by('-comment_date')
    has_unlocked = False
    if request.user.is_authenticated:
        has_unlocked = UserDwarf.objects.filter(user=request.user, dwarf=dwarf).exists()
    return render(request, 'dwarf_detail.html', {'dwarf': dwarf, 'comments': comments, 'has_unlocked': has_unlocked})


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
