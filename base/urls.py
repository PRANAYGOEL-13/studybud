# this is the file where we store all the urls that are going to be in our app


from django.urls import path
from . import views


urlpatterns = [

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    
    
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),#<str:pk> pk is the dynamic value for the room id 
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),#<str:pk> pk is the dynamic value for the room id 
    
    
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activities/', views.activityPage, name="activity"),

]
