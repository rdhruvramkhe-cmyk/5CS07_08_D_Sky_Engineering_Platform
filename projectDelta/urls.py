from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # accounts: login, logout, signup
    path('', CustomLoginView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),

    # teams: dashboard, team list, team detail, schedule
    path('teams/', include('teams.urls')),

    # sky: organisation, departments (Hisham Suleman - Student 2)
    path('', include('sky.urls')),

    # reports: dashboard, exports (Student 5)
    path('reports/', include('reports.urls')),
]

