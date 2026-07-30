from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add-hall/', views.add_hall, name='add_hall'),
    path('hall-list/', views.hall_list, name='hall_list'),
    path('book-hall/', views.book_hall, name='book_hall'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('edit-hall/<int:id>/', views.edit_hall, name='edit_hall'),
    path('delete-hall/<int:id>/', views.delete_hall, name='delete_hall'),
]