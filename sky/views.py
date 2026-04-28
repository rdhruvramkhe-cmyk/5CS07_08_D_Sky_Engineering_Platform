# views.py
# Author: Hisham Suleman
# Views for the Organisation/Department/Team panel
# Uses teams.models as the shared group data source
# All views require login — unauthenticated users are redirected to /accounts/login/

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from teams.models import Department, Team, Dependency


@login_required(login_url='/accounts/login/')
def organisation_view(request):
    # prefetch_related fetches all teams in one query rather than one per department
    departments = Department.objects.prefetch_related('teams').all()
    dependencies = Dependency.objects.select_related(
        'source_team', 'target_team'
    ).all()
    return render(request, 'sky/organisation.html', {
        'departments': departments,
        'dependencies': dependencies,
    })


@login_required(login_url='/accounts/login/')
def department_list(request):
    query = request.GET.get('q', '')
    departments = Department.objects.prefetch_related('teams')
    if query:
        # icontains means case-insensitive so 'xtv' matches 'xTV_Web'
        departments = departments.filter(department_name__icontains=query)
    return render(request, 'sky/department_list.html', {
        'departments': departments,
        'query': query,
    })


@login_required(login_url='/accounts/login/')
def department_detail(request, department_id):
    # 404 if department doesn't exist rather than crashing
    department = get_object_or_404(Department, pk=department_id)
    # prefetch all related data in one go to avoid hitting the database for every team
    teams = department.teams.prefetch_related(
        'members__user',
        'outgoing_dependencies__target_team',
        'incoming_dependencies__source_team',
        'contact_channels',
        'repositories'
    ).all()
    return render(request, 'sky/department_detail.html', {
        'department': department,
        'teams': teams,
    })


@login_required(login_url='/accounts/login/')
def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    # upstream = teams this team depends on, downstream = teams that depend on this team
    upstream = team.outgoing_dependencies.select_related('target_team').all()
    downstream = team.incoming_dependencies.select_related('source_team').all()
    return render(request, 'sky/team_detail.html', {
        'team': team,
        'upstream': upstream,
        'downstream': downstream,
    })
