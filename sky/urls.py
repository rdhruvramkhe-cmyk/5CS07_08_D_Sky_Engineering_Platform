from django.urls import path
from . import views

urlpatterns = [
    path('organisation/', views.organisation_view, name='organisation'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:department_id>/', views.department_detail, name='department_detail'),
    path('sky/teams/<int:team_id>/', views.team_detail, name='sky_team_detail'),
]
