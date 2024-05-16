# Autorzy: Jonasz Lazar, Kacper Malinowski

from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)  # Importowanie widoków do obsługi tokenów JWT.

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),  # Strona główna.
    path('user/', views.UserView.as_view(), name='user_detail'),  # Szczegóły użytkownika.
    path('register/', views.RegisterView.as_view(), name='register'),  # Rejestracja.
    path('logout/', views.LogoutView.as_view(), name='logout'),  # Wylogowanie.
    path('dwarfs/', views.DwarfListView.as_view(), name='dwarfs'),  # Lista krasnoludów.
    path('dwarfs/<int:pk>/', views.DwarfDetailView.as_view(), name='dwarf_detail'),  # Szczegóły krasnoluda.
    path('dwarfs/<int:pk>/qr_code/', views.GenerateQRCodeView.as_view(), name='generate_qr_code'),  # Generowanie kodu QR.
    path('dwarfs/<int:pk>/comments/', views.CommentCreateView.as_view(), name='comment_create'),  # Tworzenie komentarza.
    path('comments/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),  # Usuwanie komentarza.
    path('verify_qr_code/', views.VerifyQRCodeView.as_view(), name='verify_qr_code'),  # Weryfikacja kodu QR.
    path('users_ranking/', views.UserRankingView.as_view(), name='users_ranking'),  # Ranking użytkowników.
    path('user_comments/', views.UserCommentsView.as_view(), name='user_comments'),  # Komentarze użytkownika.
    path('user_achievements/', views.UserAchievementsView.as_view(), name='user_achievements'),  # Osiągnięcia użytkownika.
    path('achievements_to_gain/', views.AchievementsToGainView.as_view(), name='achievements_to_gain'),  # Osiągnięcia do zdobycia.
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Pobieranie pary tokenów.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Odświeżanie tokena.
]
