from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=64)
    joined_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'users'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


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
    description = models.TextField()

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
