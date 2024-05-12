# Autorzy: Jonasz Lazar, Kacper Malinowski

from rest_framework import serializers
from .models import User, Dwarf, UserDwarf, Comment, Achievement, UserAchievement
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    num_dwarfs = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'num_dwarfs', 'num_comments']

    def get_num_dwarfs(self, obj):
        return UserDwarf.objects.filter(user=obj).count()

    def get_num_comments(self, obj):
        return Comment.objects.filter(user=obj).count()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {
            'username': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class DwarfSerializer(serializers.ModelSerializer):
    is_unlocked = serializers.SerializerMethodField()

    class Meta:
        model = Dwarf
        fields = ['id', 'name', 'author', 'address', 'location', 'description', 'image_url', 'is_unlocked']

    def get_is_unlocked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserDwarf.objects.filter(user=user, dwarf=obj).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    dwarf = DwarfSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'dwarf', 'comment_text', 'comment_date']

    def create(self, validated_data):
        user = self.context['request'].user
        return Comment.objects.create(user=user, **validated_data)


class DwarfDetailSerializer(serializers.ModelSerializer):
    is_unlocked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    user_comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Dwarf
        fields = ['id', 'name', 'author', 'address', 'location', 'description', 'image_url', 'is_unlocked', 'comments',
                  'user_comments_count']

    def get_is_unlocked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserDwarf.objects.filter(user=user, dwarf=obj).exists()
        return False

    def get_user_comments_count(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Comment.objects.filter(user=user, dwarf=obj).count()
        return 0


class CommentCreateSerializer(serializers.ModelSerializer):
    comment_text = serializers.CharField(required=True)

    class Meta:
        model = Comment
        fields = ['comment_text']


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['name', 'description', 'badge_icon']


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ['achievement', 'achievement_date']
