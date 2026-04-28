from django.db.models import Count, Q

from teams.models import ContactChannel, Department, Repository, Team, Dependency


def build_reports_snapshot():
    # In our Team model, the manager/leader is stored in the team_leader field.
    # A team has no manager if team_leader is empty/null.
    unmanaged_filter = Q(team_leader__isnull=True)

    # Count how many teams belong to each department.
    team_count_by_department = (
        Department.objects
        .annotate(team_count=Count('teams'))
        .order_by('-team_count', 'department_name')
    )

    # List teams that do not currently have a team leader assigned.
    teams_without_managers = (
        Team.objects
        .filter(unmanaged_filter)
        .select_related('department')
        .order_by('department__department_name', 'team_name')
    )

    summary_rows = []

    # Build a summary row for each department.
    for department in Department.objects.prefetch_related(
        'teams__repositories',
        'teams__contact_channels'
    ):
        teams = list(department.teams.all())

        summary_rows.append({
            'department': department,
            'team_count': len(teams),
            'manager_count': sum(1 for team in teams if team.team_leader),
            'repository_count': sum(team.repositories.count() for team in teams),
            'contact_channel_count': sum(team.contact_channels.count() for team in teams),
        })

    # Sort departments by number of teams, then by department name.
    summary_rows.sort(
        key=lambda row: (-row['team_count'], row['department'].department_name)
    )

    return {
        'stats': {
            'total_teams': Team.objects.count(),
            'total_departments': Department.objects.count(),
            'total_dependencies': Dependency.objects.count(),
            'total_repositories': Repository.objects.count(),
            'total_contact_channels': ContactChannel.objects.count(),
            'teams_without_managers': teams_without_managers.count(),
            'teams_with_managers': Team.objects.exclude(unmanaged_filter).count(),
        },
        'team_count_by_department': team_count_by_department,
        'summary_rows': summary_rows,
        'teams_without_managers': teams_without_managers,
    }