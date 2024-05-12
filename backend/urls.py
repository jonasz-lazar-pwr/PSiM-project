# Autorzy: Jonasz Lazar, Kacper Malinowski

from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('user/', views.UserView.as_view(), name='user_detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dwarfs/', views.DwarfListView.as_view(), name='dwarfs'),
    path('dwarfs/<int:pk>/', views.DwarfDetailView.as_view(), name='dwarf_detail'),
    path('dwarfs/<int:pk>/qr_code/', views.GenerateQRCodeView.as_view(), name='generate_qr_code'),
    path('dwarfs/<int:pk>/comments/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('verify_qr_code/', views.VerifyQRCodeView.as_view(), name='verify_qr_code'),
    path('users_ranking/', views.UserRankingView.as_view(), name='users_ranking'),
    path('user_comments/', views.UserCommentsView.as_view(), name='user_comments'),
    path('user_achievements/', views.UserAchievementsView.as_view(), name='user_achievements'),
    path('achievements_to_gain/', views.AchievementsToGainView.as_view(), name='achievements_to_gain'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
