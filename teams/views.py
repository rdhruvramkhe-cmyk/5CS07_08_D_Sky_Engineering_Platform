"""
Author : Dhruv Ramkhalawon

Description : This file contains the main view functions for the Sky Engineering portal .
It handles the dashboard, team listing, team details and meeting scheduling.

"""

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render, redirect
from .models import Team, Department, Skill, Meeting
from django.db.models.functions import TruncWeek

#Dashboard Page
#This shows the main summary of the system such as total teams,
#Departments, skills, upcoming meetings and chart data

@login_required
def dashboard(request):

    #Main numbers shown in the KPI Cards
    total_teams = Team.objects.count()
    total_departments = Department.objects.count()
    total_skills = Skill.objects.count()

    #Shows the next 10 meetings on the dashboard
    upcoming_meetings = Meeting.objects.select_related('team').order_by('date_time')[:10]

    # Data for the "Teams by Department" chart
    teams_by_department = Department.objects.annotate(team_count=Count('teams'))

    dept_labels = []
    dept_counts = []

    for department in teams_by_department:
        dept_labels.append(department.department_name)
        dept_counts.append(department.team_count)

    #Data for the "Meetings per Week" Chart
    meetings_by_week = (
        Meeting.objects
        .annotate(week=TruncWeek('date_time'))
        .values('week')
        .annotate(meeting_count=Count('id'))
        .order_by('week')
    )

    meeting_labels = []
    meeting_counts = []

    for meeting in meetings_by_week:
        if meeting['week']:
            meeting_labels.append("Week Of " + meeting['week'].strftime('%d %b'))
            meeting_counts.append(meeting['meeting_count'])


    return render(request, 'teams/dashboard.html', {
        'total_teams': total_teams,
        'total_departments': total_departments,
        'total_skills': total_skills,
        'upcoming_meetings': upcoming_meetings,
        'dept_labels': dept_labels,
        'dept_counts': dept_counts,
        'meeting_labels': meeting_labels,
        'meeting_counts': meeting_counts,

    })

#Teams Directory Page
#This allows users to search and filter teams by name, department or skill.
@login_required
def team_list(request):

    #Get search/filter values from the URL
    query = request.GET.get('q', '').strip()
    department = request.GET.get('department', '').strip()
    skill = request.GET.get('skill', '').strip()

    #Main List of Active Teams
    teams = Team.objects.select_related('department', 'team_leader').prefetch_related(
        'skills',
        'contact_channels'
    ).filter(is_active=True).order_by('team_name')

    #Search by team name, description, mission, leader or department
    if query:
        teams = teams.filter(
            Q(team_name__icontains=query) |
            Q(description__icontains=query) |
            Q(mission__icontains=query) |
            Q(team_leader__username__icontains=query) |
            Q(team_leader__first_name__icontains=query) |
            Q(team_leader__last_name__icontains=query) |
            Q(department__department_name__icontains=query)
        )

    #Filter by department if selected
    if department:
        teams = teams.filter(department_id=department)

    #Filter by skill if selected
    if skill:
        teams = teams.filter(skills__id=skill)

    #These are used to fill the dropdowns in the search form
    departments = Department.objects.all().order_by('department_name')
    skills = Skill.objects.all().order_by('skill_name')

    return render(request, 'teams/team_list.html', {
        'teams': teams,
        'departments': departments,
        'skills': skills,
        'query': query,
        'selected_department': department,
        'selected_skill': skill,
    })

#Team Detail Page
#This shows all information about one selected team
@login_required
def team_detail(request, team_id):
    team = get_object_or_404(
        Team.objects.select_related('department', 'team_leader').prefetch_related(
            'skills',
            'repositories',
            'contact_channels',
            'channels',
            'members',
            'outgoing_dependencies',
            'incoming_dependencies'
        ),
        id=team_id
    )

    return render(request, 'teams/team_detail.html', {
        'team': team,
    })

#Schedule Meeting Page
#This lets a logged-in user to create a meeting for a selected team
@login_required
def schedule_meeting(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == "POST":
        date_time = request.POST.get("date_time")
        platform = request.POST.get("platform")
        message = request.POST.get("message")

        #Save the meeting to the database
        Meeting.objects.create(
            team=team,
            scheduled_by=request.user,
            date_time=date_time,
            platform=platform,
            message=message,
            status = "Scheduled"
        )

        #Sends the user back to the team page after creating the meeting
        return redirect('team_detail', team_id=team_id)
    
    return render(request, 'teams/schedule_meeting.html',{
        'team':team
    })
    