from django.urls import path
from . import views

urlpatterns = [
    path('', views.recruitment_list_view, name='recruitment-list'),
    path('<int:pk>/', views.recruitment_detail_view, name='recruitment-detail'),
    path('create/', views.recruitment_create_view, name='recruitment-create'),
    path('<int:pk>/apply/', views.recruitment_apply_view, name='recruitment-apply'),
    path('<int:pk>/application/<int:app_id>/<str:action>/', views.recruitment_application_action_view, name='recruit-app-action'),
]
