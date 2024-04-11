from django.urls import path
from app import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('dwarfs/', views.dwarfs_list_view, name='dwarfs_list'),
    path('dwarfs/<int:pk>/', views.dwarf_detail_view, name='dwarf_detail'),
    path('dwarfs/<int:pk>/qr/', views.generate_qr_code, name='dwarf_qr_code'),
    path('dwarfs/<int:pk>/comment/create/', views.dwarf_comment_create_view, name='dwarf_comment_create'),
    path('dwarfs/<int:pk>/comment/delete/', views.dwarf_comment_delete_view, name='dwarf_comment_delete'),
    path('ranking/', views.users_ranking_view, name='users_ranking'),
    path('my_comments/', views.user_comments_view, name='user_comments'),
    path('my_achievements/', views.user_achievements_view, name='user_achievements'),
    path('scan_qr_code/', views.scan_qr_code, name='scan_qr_code'),
    path('verify_qr_code', views.verify_qr_code, name='verify_qr_code')
]
