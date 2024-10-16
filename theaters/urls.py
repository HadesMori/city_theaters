from django.urls import path
from . import views

urlpatterns = [
    path('', views.performance_list, name='performance_list'),
    path('performance/<int:pk>/', views.PerformanceDetailView.as_view(), name='performance_detail'),
    path('theater/<int:pk>/', views.TheaterDetailView.as_view(), name='theater_detail'),
]