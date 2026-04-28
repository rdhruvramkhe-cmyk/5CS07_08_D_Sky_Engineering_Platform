from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    head_name = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='teams',
    )
    team_leader_name = models.CharField(max_length=100, blank=True)
    jira_project_name = models.CharField(max_length=150, blank=True)
    workstream = models.CharField(max_length=150, blank=True)
    development_focus = models.TextField(blank=True)
    key_skills = models.TextField(blank=True)
    purpose = models.TextField(blank=True)
    software_owned = models.TextField(blank=True)
    versioning_approaches = models.TextField(blank=True)
    wiki_search_terms = models.TextField(blank=True)
    team_wiki_url = models.URLField(blank=True)
    concurrent_projects = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['department__name', 'name']

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ['team__name', 'name']

    def __str__(self):
        return f'{self.name} ({self.team.name})'


class Repository(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(max_length=150)
    url = models.URLField()

    class Meta:
        ordering = ['team__name', 'name']

    def __str__(self):
        return f'{self.team.name}: {self.name}'


class ContactChannel(models.Model):
    class ChannelType(models.TextChoices):
        SLACK = 'SLACK', 'Slack'
        STANDUP = 'STANDUP', 'Standup'
        EMAIL = 'EMAIL', 'Email'
        OTHER = 'OTHER', 'Other'

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='contact_channels')
    channel_type = models.CharField(max_length=20, choices=ChannelType.choices)
    label = models.CharField(max_length=150)
    value = models.CharField(max_length=255)

    class Meta:
        ordering = ['team__name', 'channel_type', 'label']

    def __str__(self):
        return f'{self.team.name}: {self.label}'


class TeamDependency(models.Model):
    source_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='downstream_dependencies',
    )
    target_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='upstream_dependencies',
    )
    dependency_type = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['source_team__name', 'target_team__name']
        constraints = [
            models.UniqueConstraint(
                fields=['source_team', 'target_team', 'dependency_type'],
                name='unique_team_dependency',
            ),
        ]

    def __str__(self):
        return f'{self.source_team.name} -> {self.target_team.name}'


class AuditLog(models.Model):
    action = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.action} @ {self.created_at:%Y-%m-%d %H:%M}'
