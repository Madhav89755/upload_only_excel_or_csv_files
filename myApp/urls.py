from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView, name='login_page'),
    path('homepage/', views.homeView, name='homepage'),
    path('deleteFile/<int:pk>', views.deleteFileView, name='delete_file'),
    path('upload-file/', views.uploadFileView, name='upload_file_page'),
    path('show-data/<int:pk>', views.showDataView, name='show_data_page'),
    path('register/', views.registerView, name='register_page'),
    path('logout/', views.logoutView, name='logout'),
]
