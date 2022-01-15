from django.urls import path

from . import views


urlpatterns = [
    path('', views.loginPage, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register/', views.registerPage, name='register'),
    
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('posts/', views.posts, name='posts'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    
    path('create_ticket/', views.createTicket, name='create_ticket'),
    path('update_ticket/<str:pk>', views.updateTicket, name='update_ticket'),
] 