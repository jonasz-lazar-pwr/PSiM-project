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
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Dwarf(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.TextField()

    class Meta:
        managed = True
        db_table = 'dwarfs'
        verbose_name_plural = 'Dwarfs'

    @property
    def comments(self):
        return self.comment_set.all()

    def __str__(self):
        return self.name


class UserDwarf(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dwarf = models.ForeignKey(Dwarf, on_delete=models.CASCADE)
    visited_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'userdwarfs'
        verbose_name_plural = 'UserDwarfs'

    def __str__(self):
        return f'{self.user.username} - {self.dwarf.name}'


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dwarf = models.ForeignKey(Dwarf, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'comments'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.comment_text


class Achievement(models.Model):
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
