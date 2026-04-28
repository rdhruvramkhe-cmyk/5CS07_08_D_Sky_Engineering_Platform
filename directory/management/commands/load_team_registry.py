import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from directory.models import AuditLog, ContactChannel, Department, Repository, Team, TeamDependency


def split_values(raw_value):
    return [item.strip() for item in raw_value.split(',') if item.strip()]


def normalize_url(value):
    value = (value or '').strip()
    if not value:
        return ''
    if value.startswith(('http://', 'https://')):
        return value
    return f'https://{value}'


class Command(BaseCommand):
    help = 'Loads the Sky team registry seed data into SQLite.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--replace',
            action='store_true',
            help='Replace existing team data before importing.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        source_file = settings.BASE_DIR / 'seed_data' / 'team_registry_rows.json'
        rows = json.loads(Path(source_file).read_text(encoding='utf-8'))
        rows = [row for row in rows if row.get('Team Name', '').strip()]

        if options['replace']:
            TeamDependency.objects.all().delete()
            ContactChannel.objects.all().delete()
            Repository.objects.all().delete()
            Team.objects.all().delete()
            Department.objects.all().delete()

        for row in rows:
            department, _ = Department.objects.get_or_create(
                name=row.get('Department', '').strip(),
                defaults={'head_name': row.get('Department Head', '').strip()},
            )
            if row.get('Department Head', '').strip() and department.head_name != row['Department Head'].strip():
                department.head_name = row['Department Head'].strip()
                department.save(update_fields=['head_name', 'updated_at'])

            team, _ = Team.objects.update_or_create(
                name=row.get('Team Name', '').strip(),
                defaults={
                    'department': department,
                    'team_leader_name': row.get('Team Leader', '').strip(),
                    'jira_project_name': row.get('Jira Project Name', '').strip(),
                    'workstream': row.get('Workstream (MF)', '').strip().replace('#REF!', ''),
                    'development_focus': row.get('Development Focus Areas', '').strip(),
                    'key_skills': row.get('Key Skills & Technologies', '').strip(),
                    'purpose': row.get('Development Focus Areas', '').strip(),
                    'software_owned': row.get('Software Owned and Evolved By This Team', '').strip(),
                    'versioning_approaches': row.get('Versioning Approaches', '').strip(),
                    'wiki_search_terms': row.get('Wiki Search Terms', '').strip(),
                    'team_wiki_url': normalize_url(row.get('Team Wiki', '')),
                    'concurrent_projects': row.get(' # of Concurrent Projects', '').strip(),
                },
            )

            Repository.objects.filter(team=team).delete()
            repo_url = normalize_url(row.get('Project (codebase) (Github Repo)', ''))
            if repo_url:
                Repository.objects.create(
                    team=team,
                    name=f'{team.name} codebase',
                    url=repo_url,
                )

            ContactChannel.objects.filter(team=team).delete()
            for index, channel in enumerate(split_values(row.get('Slack Channels', '')), start=1):
                ContactChannel.objects.create(
                    team=team,
                    channel_type=ContactChannel.ChannelType.SLACK,
                    label=f'Slack channel {index}',
                    value=channel,
                )
            standup = row.get('Daily Standup Time and Link', '').strip()
            if standup:
                ContactChannel.objects.create(
                    team=team,
                    channel_type=ContactChannel.ChannelType.STANDUP,
                    label='Daily standup',
                    value=standup,
                )

        TeamDependency.objects.all().delete()
        team_lookup = {team.name: team for team in Team.objects.select_related('department')}
        for row in rows:
            source_team = team_lookup.get(row.get('Team Name', '').strip())
            for dependency_name in split_values(row.get('Downstream Dependencies', '')):
                target_team = team_lookup.get(dependency_name)
                if not source_team or not target_team:
                    continue
                TeamDependency.objects.get_or_create(
                    source_team=source_team,
                    target_team=target_team,
                    dependency_type=row.get('Dependency Type', '').strip(),
                )

        AuditLog.objects.create(
            action='team_registry_import',
            details=f'Imported {len(rows)} teams from {source_file.name}.',
        )
        self.stdout.write(self.style.SUCCESS(f'Imported {len(rows)} teams from {source_file.name}.'))
