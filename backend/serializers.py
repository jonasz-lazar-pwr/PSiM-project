# Autorzy: Jonasz Lazar, Kacper Malinowski

from rest_framework import serializers
from .models import User, Dwarf, UserDwarf, Comment, Achievement, UserAchievement
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    """
    Serializator dla modelu User.

    Jest używany do konwersji obiektów User na format JSON i odwrotnie.
    Zawiera pola: 'id', 'username', 'num_dwarfs', 'num_comments'.
    """
    num_dwarfs = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'num_dwarfs', 'num_comments']

    def get_num_dwarfs(self, obj):
        """
        Metoda zwracająca liczbę krasnoludków przypisanych do użytkownika.

        Jest wywoływana, gdy serializowany jest obiekt User.
        Zwraca liczbę obiektów UserDwarf, które są przypisane do danego użytkownika.
        """
        return UserDwarf.objects.filter(user=obj).count()

    def get_num_comments(self, obj):
        """
        Metoda zwracająca liczbę komentarzy dodanych przez użytkownika.

        Jest wywoływana, gdy serializowany jest obiekt User.
        Zwraca liczbę obiektów Comment, które są przypisane do danego użytkownika.
        """
        return Comment.objects.filter(user=obj).count()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializator dla procesu rejestracji użytkownika.

    Ten serializator jest używany do walidacji danych wprowadzanych przez użytkownika podczas rejestracji.
    Zawiera pola: 'username', 'password', 'password2'.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {
            'username': {'required': True},
        }

    def validate(self, attrs):
        """
        Metoda walidacji danych.

        Sprawdza, czy hasła wprowadzone przez użytkownika są identyczne.
        Jeśli nie, zgłasza błąd walidacji.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        """
        Metoda tworzenia nowego użytkownika.

        Po pomyślnej walidacji danych, tworzy nowego użytkownika z danymi wprowadzonymi przez użytkownika.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class DwarfSerializer(serializers.ModelSerializer):
    """
    Serializator dla modelu Dwarf.

    Jest używany do konwersji obiektów Dwarf na format JSON i odwrotnie.
    Zawiera pola: 'id', 'name', 'author', 'address', 'location', 'description', 'image_url', 'is_unlocked'.
    """
    is_unlocked = serializers.SerializerMethodField()

    class Meta:
        model = Dwarf
        fields = ['id', 'name', 'author', 'address', 'location', 'description', 'image_url', 'is_unlocked']

    def get_is_unlocked(self, obj):
        """
        Metoda zwracająca informację, czy dany krasnoludek jest odblokowany dla zalogowanego użytkownika.

        Jest wywoływana, gdy serializowany jest obiekt Dwarf.
        Zwraca True, jeśli zalogowany użytkownik odblokował danego krasnoludka, w przeciwnym razie zwraca False.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            return UserDwarf.objects.filter(user=user, dwarf=obj).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializator dla modelu Comment.

    Jest używany do konwersji obiektów Comment na format JSON i odwrotnie.
    Zawiera pola: 'id', 'user', 'dwarf', 'comment_text', 'comment_date'.
    """
    user = UserSerializer(read_only=True)
    dwarf = DwarfSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'dwarf', 'comment_text', 'comment_date']

    def create(self, validated_data):
        """
        Metoda tworzenia nowego komentarza.

        Po pomyślnej walidacji danych, tworzy nowy komentarz z danymi wprowadzonymi przez użytkownika.
        """
        user = self.context['request'].user
        return Comment.objects.create(user=user, **validated_data)


class DwarfDetailSerializer(serializers.ModelSerializer):
    """
    Serializator dla szczegółów modelu Dwarf.

    Jest używany do konwersji obiektów Dwarf na format JSON i odwrotnie.
    Zawiera pola: 'id', 'name', 'author', 'address', 'location', 'description', 'image_url', 'is_unlocked', 'comments',
    'user_comments_count'.
    """
    is_unlocked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    user_comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Dwarf
        fields = ['id', 'name', 'author', 'address', 'location', 'description', 'image_url', 'is_unlocked', 'comments',
                  'user_comments_count']

    def get_is_unlocked(self, obj):
        """
        Metoda zwracająca informację, czy dany krasnoludek jest odblokowany dla zalogowanego użytkownika.

        Jest wywoływana, gdy serializowany jest obiekt Dwarf.
        Zwraca True, jeśli zalogowany użytkownik odblokował danego krasnoludka, w przeciwnym razie zwraca False.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            return UserDwarf.objects.filter(user=user, dwarf=obj).exists()
        return False

    def get_user_comments_count(self, obj):
        """
        Metoda zwracająca liczbę komentarzy dodanych przez zalogowanego użytkownika do danego krasnoludka.

        Jest wywoływana, gdy serializowany jest obiekt Dwarf.
        Zwraca liczbę obiektów Comment, które są przypisane do danego użytkownika i krasnoludka.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            return Comment.objects.filter(user=user, dwarf=obj).count()
        return 0


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializator do tworzenia instancji modelu Comment.

    Ten serializator jest używany do konwersji obiektów Comment na format JSON i odwrotnie.
    Zawiera tylko pole 'comment_text', które jest wymagane.
    """
    comment_text = serializers.CharField(required=True)

    class Meta:
        model = Comment
        fields = ['comment_text']


class AchievementSerializer(serializers.ModelSerializer):
    """
    Serializator dla modelu Achievement.

    Jest używany do konwersji obiektów Achievement na format JSON i odwrotnie.
    Zawiera pola: 'name', 'description', 'badge_icon'.
    """
    class Meta:
        model = Achievement
        fields = ['name', 'description', 'badge_icon']


class UserAchievementSerializer(serializers.ModelSerializer):
    """
    Serializator dla modelu UserAchievement.

    Jest używany do konwersji obiektów UserAchievement na format JSON i odwrotnie.
    Zawiera pola: 'achievement', 'achievement_date'.
    """
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ['achievement', 'achievement_date']
