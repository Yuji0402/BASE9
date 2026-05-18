from django.urls import path
from . import views

urlpatterns = [
    path('', views.ground_list_view, name='ground-list'),
    path('<int:pk>/', views.ground_detail_view, name='ground-detail'),
    path('create/', views.ground_create_view, name='ground-create'),
    path('<int:ground_pk>/reserve/', views.reservation_create_view, name='reservation-create'),
]
