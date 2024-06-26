# Autorzy: Jonasz Lazar, Kacper Malinowski

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Model reprezentująca użytkownika.
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    joined_date = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    def __str__(self):
        """
        Zwraca reprezentację tekstową obiektu.
        """
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Dwarf(models.Model):
    """
    Model reprezentująca krasnoludka.
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.TextField()

    class Meta:
        managed = True  # Django zarządza tym modelem.
        db_table = 'dwarfs'  # Nazwa tabeli w bazie danych.
        verbose_name_plural = 'Dwarfs'  # Nazwa modelu w liczbie mnogiej.

    @property
    def comments(self):
        """
        Zwraca wszystkie komentarze do tego krasnoluda.
        """
        return self.comment_set.all()

    def __str__(self):
        """
        Zwraca reprezentację tekstową obiektu.
        """
        return self.name


class UserDwarf(models.Model):
    """
    Model reprezentujący relację między użytkownikiem a krasnoludem.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dwarf = models.ForeignKey(Dwarf, on_delete=models.CASCADE)
    visited_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True  # Django zarządza tym modelem.
        db_table = 'userdwarfs'  # Nazwa tabeli w bazie danych.
        verbose_name_plural = 'UserDwarfs'  # Nazwa modelu w liczbie mnogiej.

    def __str__(self):
        """
        Zwraca reprezentację tekstową obiektu.
        """
        return f'{self.user.username} - {self.dwarf.name}'


class Comment(models.Model):
    """
    Model reprezentujący komentarz.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dwarf = models.ForeignKey(Dwarf, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True  # Django zarządza tym modelem.
        db_table = 'comments'  # Nazwa tabeli w bazie danych.
        verbose_name_plural = 'Comments'  # Nazwa modelu w liczbie mnogiej.

    def __str__(self):
        """
        Zwraca reprezentację tekstową obiektu.
        """
        return self.comment_text


class Achievement(models.Model):
    """
    Model reprezentujący osiągnięcie.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    comment_count = models.IntegerField()
    dwarf_count = models.IntegerField()
    description = models.TextField()
    badge_icon = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'achievements'
        verbose_name_plural = 'Achievements'

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """
    Model reprezentujący relację między użytkownikiem a osiągnięciem.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achievement_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'userachievements'
        verbose_name_plural = 'UserAchievements'

    def __str__(self):
        return f'{self.user.username} - {self.achievement.name}'
