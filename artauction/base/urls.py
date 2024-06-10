from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<str:pk>/', views.item, name='item'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<str:pk>/', views.user_profile, name='user-profile'),
    path('update-user/', views.update_user, name='update-user'),
    path('create-item/', views.create_item, name='create-item'),
    path('delete-item/<str:pk>/', views.delete_item, name='delete-item'),
]