from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('', views.team_list, name = 'teams_list'),
    path('<int:team_id>/', views.team_detail, name='team_detail'),
    path('schedule/<int:team_id>/', views.schedule_meeting, name='schedule_meeting'),
]
