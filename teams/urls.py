from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list_view, name='team-list'),
    path('<int:pk>/', views.team_detail_view, name='team-detail'),
    path('create/', views.team_create_view, name='team-create'),
    path('<int:pk>/edit/', views.team_edit_view, name='team-edit'),
    path('<int:pk>/join/', views.team_join_view, name='team-join'),
    path('<int:pk>/member/<int:user_id>/<str:action>/', views.membership_action_view, name='membership-action'),
]
