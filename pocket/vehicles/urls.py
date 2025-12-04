from django.urls import path
from . import views

urlpatterns = [
     path("login/", views.my_login, name="my-login"),
    path("register/", views.register, name="register"),
    path("logout/", views.user_logout, name="user_logout"),
    
    path('', views.home, name='home'),
    path('saved/', views.saved, name='saved'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('delete/<int:part_id>/', views.delete_part, name='delete_part'),
]
