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
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscriptions/<str:pk>', views.subscriptions, name='subscriptions'),
    
    path('create_ticket/', views.createTicket, name='create_ticket'),
    path('update_ticket/<str:pk>', views.updateTicket, name='update_ticket'),
    path('delete_ticket/<str:pk>', views.deleteTicket, name='delete_ticket'),
    path('create_review/', views.createTicketReview, name='create_review'),
    path('create_review/<str:pk>', views.createReview, name='create_review'),
    path('update_review/<str:pk>', views.updateReview, name='update_review'),
    path('delete_review/<str:pk>', views.deleteReview, name='delete_review'),
] 