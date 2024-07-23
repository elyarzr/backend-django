import pip
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile', views.user_profile, name='profile'),
    path('update/', views.user_update, name='update'),
    path('change/', views.change_password, name='change'),
    path('login_phone/', views.phone, name='phone'),
    path('verify/', views.verify, name='verify'),
    path('active/<uidb64>/<token>/',views.RegisterEmail.as_view(),name='active'),
]

