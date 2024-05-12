# Autorzy: Jonasz Lazar, Kacper Malinowski

from .models import UserAchievement, Achievement, Comment


def check_and_assign_dwarf_achievements(user):
    # Pobierz liczbę odwiedzonych krasnali przez użytkownika
    visited_dwarfs_count = user.userdwarf_set.count()

    # Pobierz wszystkie osiągnięcia, które użytkownik jeszcze nie zdobył
    achievements = Achievement.objects.exclude(userachievement__user=user)

    for achievement in achievements:
        # Sprawdź, czy użytkownik spełnia warunki osiągnięcia
        # i czy osiągnięcie jest związane z liczbą odwiedzonych krasnali
        if achievement.comment_count == 0 and visited_dwarfs_count >= achievement.dwarf_count:
            # Jeśli tak, przypisz osiągnięcie do użytkownika
            UserAchievement.objects.create(user=user, achievement=achievement)


def check_and_assign_comment_achievements(user):
    # Pobierz liczbę komentarzy dodanych przez użytkownika
    user_comments_count = Comment.objects.filter(user=user).count()

    # Pobierz wszystkie osiągnięcia, które użytkownik jeszcze nie zdobył
    achievements = Achievement.objects.exclude(userachievement__user=user)

    for achievement in achievements:
        # Sprawdź, czy użytkownik spełnia warunki osiągnięcia
        # i czy osiągnięcie jest związane z liczbą dodanych komentarzy
        if achievement.dwarf_count == 0 and user_comments_count >= achievement.comment_count:
            # Jeśli tak, przypisz osiągnięcie do użytkownika
            UserAchievement.objects.create(user=user, achievement=achievement)


def check_and_remove_comment_achievements(user):
    # Pobierz liczbę komentarzy dodanych przez użytkownika
    user_comments_count = Comment.objects.filter(user=user).count()

    # Pobierz wszystkie osiągnięcia, które użytkownik zdobył
    user_achievements = UserAchievement.objects.filter(user=user)

    for user_achievement in user_achievements:
        # Sprawdź, czy użytkownik nadal spełnia warunki osiągnięcia
        # i czy osiągnięcie jest związane z liczbą dodanych komentarzy
        if user_achievement.achievement.dwarf_count == 0 and user_comments_count < user_achievement.achievement.comment_count:
            # Jeśli tak, usuń osiągnięcie od użytkownika
            user_achievement.delete()
