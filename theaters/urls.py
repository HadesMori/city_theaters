from django.urls import path
from . import views

urlpatterns = [
    path('', views.performance_list, name='performance_list'),
    path('performance/<int:pk>/details/', views.PerformanceDetailView.as_view(), name='performance_detail'),  # Деталі вистави
    path('performance/<int:performance_id>/seats/', views.select_seat, name='select_seat'),  # Вибір місця
    path('ticket/confirmation/<int:seat_id>/', views.TicketConfirmationView.as_view(), name='ticket_confirmation'),  # Покупка квитка
    path('theater/<int:pk>/', views.TheaterDetailView.as_view(), name='theater_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]