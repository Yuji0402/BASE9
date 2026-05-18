from django.urls import path
from . import views

urlpatterns = [
    path('', views.match_list_view, name='match-list'),
    path('<int:pk>/', views.match_detail_view, name='match-detail'),
    path('create/', views.match_create_view, name='match-create'),
    path('<int:pk>/apply/', views.match_apply_view, name='match-apply'),
    path('<int:pk>/application/<int:app_id>/<str:action>/', views.match_application_action_view, name='match-app-action'),
]
