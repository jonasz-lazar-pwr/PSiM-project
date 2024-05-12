# Autorzy: Jonasz Lazar, Kacper Malinowski

from django.contrib import admin
from .models import User, Dwarf, UserDwarf, Comment, Achievement, UserAchievement

admin.site.register(User)
admin.site.register(Dwarf)
admin.site.register(UserDwarf)
admin.site.register(Comment)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
