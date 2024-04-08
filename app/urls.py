from django.urls import path
from app import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('dwarfs/', views.dwarfs_list_view, name='dwarfs_list'),
    path('dwarfs/<int:pk>/', views.dwarf_detail_view, name='dwarf_detail'),
    path('dwarfs/<int:pk>/comment/', views.dwarf_comment_view, name='dwarf_comment'),
    path('dwarfs/<int:pk>/comment/create/', views.dwarf_comment_create_view, name='dwarf_comment_create')
]
