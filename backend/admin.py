# Autorzy: Jonasz Lazar, Kacper Malinowski

from django.contrib import admin
from .models import User, Dwarf, UserDwarf, Comment, Achievement, UserAchievement

admin.site.register(User)  # Rejestracja modelu User w panelu administracyjnym.
admin.site.register(Dwarf)  # Rejestracja modelu Dwarf w panelu administracyjnym.
admin.site.register(UserDwarf)  # Rejestracja modelu UserDwarf w panelu administracyjnym.
admin.site.register(Comment)  # Rejestracja modelu Comment w panelu administracyjnym.
admin.site.register(Achievement)  # Rejestracja modelu Achievement w panelu administracyjnym.
admin.site.register(UserAchievement)  # Rejestracja modelu UserAchievement w panelu administracyjnym.
