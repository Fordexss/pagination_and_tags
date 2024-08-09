from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.crypto_news, name='news'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('converter/', views.converter, name='converter'),
]