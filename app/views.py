import json
import qrcode

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import CommentForm, LoginForm, RegisterForm
from .models import Achievement, Comment, Dwarf, User, UserAchievement, UserDwarf


def home_view(request):
    """
    Funkcja widoku Django obsługująca żądanie do strony głównej aplikacji.

    1. Renderuje szablon 'home.html'.
    """
    return render(request, 'home.html')


def register_view(request):
    """
    Funkcja widoku Django, która obsługuje proces rejestracji nowego użytkownika.

    1. Sprawdza, czy metoda żądania to 'POST'.
    2. Pobiera dane z formularza rejestracji.
    3. Jeżeli formularz jest prawidłowy, zapisuje nowego użytkownika i loguje go.
    4. Następnie przekierowuje użytkownika do strony głównej.
    5. Jeżeli metoda żądania nie jest 'POST', renderuje formularz rejestracji.
    """
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
    """
    Funkcja widoku Django, która obsługuje proces logowania użytkownika.

    1. Sprawdza, czy metoda żądania to 'POST'.
    2. Pobiera dane z formularza logowania.
    3. Jeżeli formularz jest prawidłowy, pobiera nazwę użytkownika i hasło z formularza.
    4. Autentykuje użytkownika za pomocą nazwy użytkownika i hasła.
    5. Jeżeli użytkownik jest prawidłowy, loguje użytkownika i przekierowuje go do strony głównej.
    6. Jeżeli użytkownik nie jest prawidłowy lub formularz nie jest prawidłowy, wyświetla błąd.
    7. Jeżeli metoda żądania nie jest 'POST', renderuje formularz logowania.
    """
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
    """
    Funkcja widoku Django, która obsługuje wyświetlanie listy krasnali.

    1. Pobiera parametr 'q' z żądania GET, który jest używany do filtrowania krasnali po nazwie.
    Jeżeli parametr 'q' nie jest podany, domyślnie wyświetla wszystkie krasnale.
    2. Pobiera wszystkie obiekty krasnali, które zawierają parametr 'q' w swojej nazwie, i sortuje je alfabetycznie.
    3. Inicjalizuje pustą listę 'user_dwarfs' i zmienną 'user_dwarfs_count' na 0.
    4. Jeżeli użytkownik jest zalogowany, pobiera listę ID krasnali, które odblokował zalogowany użytkownik,
    i zlicza liczbę tych krasnali.
    5. Renderuje szablon 'dwarfs.html', przekazując do niego listę krasnali, listę ID krasnali odblokowanych
    przez użytkownika, całkowitą liczbę krasnali i liczbę krasnali odblokowanych przez użytkownika.
    """
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
    """
    Funkcja widoku Django, która obsługuje proces tworzenia nowego komentarza dla określonego krasnala.
    Wymaga, aby użytkownik był zalogowany.

    1. Pobiera obiekt krasnala o danym kluczu głównym. Jeżeli krasnal nie istnieje, zwraca błąd 404.
    2. Sprawdza, czy zalogowany użytkownik odblokował krasnala.
    Jeżeli nie, wyświetla błąd i przekierowuje do widoku szczegółów krasnala.
    3. Zlicza liczbę komentarzy dodanych przez zalogowanego użytkownika do danego krasnala.
    Jeżeli liczba komentarzy wynosi 3 lub więcej, wyświetla błąd i przekierowuje do widoku szczegółów krasnala.
    4. Sprawdza, czy metoda żądania to 'POST'.
    5. Pobiera dane z formularza. Jeżeli formularz jest prawidłowy, tworzy nowy obiekt komentarza
    z użytkownikiem, krasnalem i tekstem komentarza.
    6. Następnie wywołuje funkcję `check_and_assign_achievements(request.user)`, aby zaktualizować osiągnięcia użytkownika.
    7. Na koniec przekierowuje użytkownika do widoku szczegółów krasnala.
    8. Jeżeli metoda żądania nie jest 'POST', renderuje formularz komentarza.
    """
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


def check_and_assign_dwarf_achievements(user):
    """
    Funkcja sprawdza i przypisuje osiągnięcia związane z krasnalami dla określonego użytkownika.
    Zapewnia, że osiągnięcia użytkownika związane z krasnalami są zawsze aktualne.

    1. Zlicza liczbę krasnali odblokowanych przez użytkownika.
    2. Pobiera wszystkie osiągnięcia, które wymagają pewnej liczby odblokowanych krasnali.
    3. Dla każdego z tych osiągnięć sprawdza, czy liczba odblokowanych krasnali przez użytkownika jest większa
    lub równa wymaganej liczbie. Jeśli tak, próbuje utworzyć nowy rekord UserAchievement dla użytkownika i osiągnięcia.
    """
    user_dwarfs_count = UserDwarf.objects.filter(user=user).count()
    all_achievements = Achievement.objects.filter(dwarf_count__gt=0)

    for achievement in all_achievements:
        if user_dwarfs_count >= achievement.dwarf_count:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user, achievement=achievement)
            if created:
                pass


def check_and_assign_comment_achievements(user):
    """
    Funkcja sprawdza i przypisuje osiągnięcia związane z komentarzami dla określonego użytkownika.
    Zapewnia, że osiągnięcia użytkownika związane z komentarzami są zawsze aktualne.

    1. Zlicza liczbę komentarzy dodanych przez użytkownika.
    2. Pobiera wszystkie osiągnięcia, które wymagają pewnej liczby komentarzy.
    3. Dla każdego z tych osiągnięć sprawdza, czy liczba komentarzy użytkownika jest większa lub równa wymaganej
    liczbie. Jeśli tak, próbuje utworzyć nowy rekord UserAchievement dla użytkownika i osiągnięcia.
    4. Po przypisaniu nowych osiągnięć, funkcja następnie pobiera wszystkie rekordy UserAchievement dla użytkownika.
    5. Dla każdego z tych osiągnięć użytkownika sprawdza, czy liczba komentarzy użytkownika jest mniejsza od wymaganej
    liczby. Jeśli tak, usuwa rekord UserAchievement.
    """
    user_comments_count = Comment.objects.filter(user=user).count()
    all_achievements = Achievement.objects.filter(comment_count__gt=0)

    for achievement in all_achievements:
        if user_comments_count >= achievement.comment_count:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user, achievement=achievement)
            if created:
                pass

    user_achievements = UserAchievement.objects.filter(user=user)
    for user_achievement in user_achievements:
        if user_comments_count < user_achievement.achievement.comment_count:
            user_achievement.delete()


@login_required
def user_comments_view(request):
    """
    Funkcja widoku Django, która obsługuje wyświetlanie komentarzy dodanych przez zalogowanego użytkownika.

    1. Pobiera wszystkie komentarze dodane przez zalogowanego użytkownika, sortując je malejąco według daty dodania.
    2. Renderuje szablon 'user_comments.html', przekazując do niego listę komentarzy użytkownika.
    """
    user_comments = Comment.objects.filter(user=request.user).order_by('-comment_date')
    return render(request, 'user_comments.html', {'user_comments': user_comments})


@login_required
def dwarf_comment_create_view(request, pk):
    """
    Funkcja widoku Django, która obsługuje tworzenie nowego komentarza dla określonego krasnala. Wymaga,
    aby użytkownik był zalogowany.

    1. Pobiera obiekt krasnala o danym kluczu głównym. Jeżeli krasnal nie istnieje, zwraca błąd 404.
    2. Sprawdza, czy zalogowany użytkownik odblokował krasnala.
    Jeżeli nie, wyświetla błąd i przekierowuje do widoku szczegółów krasnala.
    3. Zlicza liczbę komentarzy dodanych przez zalogowanego użytkownika do danego krasnala.
    Jeżeli liczba komentarzy wynosi 3 lub więcej, wyświetla błąd i przekierowuje do widoku szczegółów krasnala.
    4. Sprawdza, czy metoda żądania to 'POST'.
    5. Pobiera dane z formularza. Jeżeli formularz jest prawidłowy, tworzy nowy obiekt komentarza
    z użytkownikiem, krasnalem i tekstem komentarza.
    6. Następnie wywołuje funkcję `check_and_assign_comment_achievements(request.user)`, aby zaktualizować osiągnięcia.
    7. Na koniec przekierowuje użytkownika do widoku szczegółów krasnala za pomocą.
    8. Jeżeli metoda żądania nie jest 'POST', renderuje formularz komentarza.
    """
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


@login_required
def dwarf_comment_delete_view(request, pk):
    """
    Funkcja widoku Django, która obsługuje proces usuwania komentarza do określonego krasnala.

    1. Pobiera obiekt komentarza o danym kluczu głównym. Jeżeli komentarz nie istnieje, zwraca błąd 404.
    2. Sprawdza, czy zalogowany użytkownik jest autorem komentarza. Jeżeli nie, wyświetla błąd
    i przekierowuje do strony szczegółów krasnala.
    3. Jeżeli użytkownik jest autorem komentarza, usuwa komentarz.
    4. Aktualizuje osiągnięcia użytkownika związane z komentarzami.
    5. Wyświetla komunikat o pomyślnym usunięciu komentarza.
    6. Przekierowuje użytkownika do strony szczegółów krasnala.
    """
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
    """
    Funkcja widoku Django, która obsługuje wyświetlanie rankingu użytkowników.

    1. Pobiera parametr sortowania z żądania GET. Jeżeli parametr nie jest podany, domyślnie sortuje użytkowników
    według liczby odblokowanych krasnali.
    2. Pobiera wszystkich użytkowników i dodaje do nich dwie dodatkowe wartości: liczbę odblokowanych krasnali
    i liczbę dodanych komentarzy. Użytkownicy są sortowani malejąco według wybranego parametru sortowania.
    3. Renderuje szablon 'users_ranking.html', przekazując do niego listę użytkowników.
    """
    sort_by = request.GET.get('sort_by', 'num_dwarfs')
    users = User.objects.annotate(
        num_dwarfs=Count('userdwarf', distinct=True),
        num_comments=Count('comment', distinct=True)
    ).order_by('-' + sort_by)
    return render(request, 'users_ranking.html', {'users': users})


@login_required
def user_achievements_view(request):
    """
    Funkcja widoku Django, która obsługuje wyświetlanie osiągnięć użytkownika.

    1. Pobiera wszystkie osiągnięcia zalogowanego użytkownika, sortując je malejąco według daty zdobycia.
    2. Pobiera wszystkie dostępne osiągnięcia.
    3. Wyklucza z listy wszystkich osiągnięć te, które użytkownik już zdobył, tworząc listę osiągnięć do zdobycia.
    4. Renderuje szablon 'user_achievements.html', przekazując do niego listę osiągnięć użytkownika
    oraz listę osiągnięć do zdobycia.
    """
    user_achievements = UserAchievement.objects.filter(user=request.user).order_by('-achievement_date')
    all_achievements = Achievement.objects.all()
    achievements_to_gain = all_achievements.exclude(id__in=user_achievements.values_list('achievement_id', flat=True))
    return render(request, 'user_achievements.html',
                  {'user_achievements': user_achievements, 'achievements_to_gain': achievements_to_gain})


@login_required
@user_passes_test(lambda u: u.is_admin)
def generate_qr_code(request, pk):
    """
    Funkcja widoku Django, która generuje kod QR dla określonego krasnala.
    Wymaga, aby użytkownik był zalogowany i miał uprawnienia administratora.

    1. Pobiera obiekt krasnala o danym kluczu głównym. Jeżeli krasnal nie istnieje, zwraca błąd 404.
    2. Tworzy nowy obiekt QRCode z określonymi parametrami.
    3. Buduje pełny URL do widoku szczegółów krasnala i dodaje go do danych kodu QR.
    4. Generuje obraz kodu QR z określonymi kolorami.
    5. Tworzy nową odpowiedź HTTP z typem zawartości "image/png".
    6. Zapisuje obraz kodu QR do odpowiedzi w formacie PNG.
    7. Zwraca odpowiedź, która jest obrazem kodu QR.
    """
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
    """
    Funkcja widoku Django, która obsługuje proces skanowania kodu QR przez zalogowanego użytkownika.

    1. Renderuje szablon 'scan_qr_code.html'.
    """
    return render(request, 'scan_qr_code.html')


@login_required
@csrf_exempt
def verify_qr_code(request):
    """
    Funkcja widoku Django, która obsługuje proces weryfikacji skanowanego kodu QR.

    1. Sprawdza, czy metoda żądania to 'POST'.
    2. Pobiera dane z żądania i wyciąga z nich kod QR.
    3. Próbuje pobrać obiekt krasnala, którego klucz główny jest zawarty w kodzie QR.
    Jeżeli krasnal nie istnieje, zwraca błąd JSON z komunikatem o nieprawidłowym kodzie QR.
    4. Próbuje utworzyć nowy rekord UserDwarf dla zalogowanego użytkownika i krasnala.
    Jeżeli rekord już istnieje, zwraca błąd JSON z komunikatem, że krasnal został już odblokowany.
    5. Jeżeli rekord UserDwarf został utworzony, aktualizuje osiągnięcia użytkownika.
    6. Zwraca odpowiedź JSON z informacją o sukcesie i adresem URL do widoku szczegółów krasnala.
    7. Jeżeli metoda żądania nie jest 'POST', zwraca błąd JSON z komunikatem o nieprawidłowym żądaniu.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        qr_code = data.get('qr_code')
        try:
            dwarf = Dwarf.objects.get(pk=qr_code.split('/')[-2])
            user_dwarf, created = UserDwarf.objects.get_or_create(user=request.user, dwarf=dwarf)
            if created:
                check_and_assign_dwarf_achievements(request.user)
                return JsonResponse({'success': True, 'url': reverse('dwarf_detail', args=[dwarf.id])})
            else:
                return JsonResponse({'success': False, 'message': 'Ten krasnal został już odblokowany.',
                                     'url': reverse('dwarf_detail', args=[dwarf.id])})
        except Dwarf.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Nieprawidłowy kod QR.'})
    else:
        return JsonResponse({'success': False, 'message': 'Nieprawidłowe żądanie.'})
