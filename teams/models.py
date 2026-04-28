from django.db import models
from django.contrib.auth.models import User


# ─────────────────────────────────────────
#  DEPARTMENT
# ─────────────────────────────────────────
class Department(models.Model):
    department_name = models.CharField(max_length=200, unique=True, default='Unknown')
    department_description = models.TextField(blank=True, default='')
    department_head = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )

    def __str__(self):
        return self.department_name


# ─────────────────────────────────────────
#  ROLE
# ─────────────────────────────────────────
class Role(models.Model):
    role_name = models.CharField(max_length=100, unique=True, default='Unknown')
    role_description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.role_name


# ─────────────────────────────────────────
#  SKILL
# ─────────────────────────────────────────
class Skill(models.Model):
    skill_name = models.CharField(max_length=100, unique=True)
    skill_description = models.TextField(blank=True)

    def __str__(self):
        return self.skill_name


# ─────────────────────────────────────────
#  TEAM
# ─────────────────────────────────────────
class Team(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='teams',
        null=True,
        blank=True
    )
    team_leader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='led_teams'
    )
    team_name = models.CharField(max_length=200, default='Unknown')
    mission = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name='teams'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.team_name


# ─────────────────────────────────────────
#  TEAM MEMBER
# ─────────────────────────────────────────
class TeamMember(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='team_memberships'
    )
    role_in_team = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.team.team_name}"


# ─────────────────────────────────────────
#  DEPENDENCY
# ─────────────────────────────────────────
class Dependency(models.Model):
    DEPENDENCY_TYPES = [
        ('infrastructure', 'Infrastructure Support'),
        ('bug', 'Bug Resolution'),
        ('security', 'Security Fixes'),
        ('deployment', 'Deployment Pipeline'),
        ('agile', 'Agile Coaching'),
        ('api', 'API Integration'),
        ('other', 'Other'),
    ]
    source_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='outgoing_dependencies',
        null=True,
        blank=True
    )
    target_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='incoming_dependencies',
        null=True,
        blank=True
    )
    dependency_type = models.CharField(
        max_length=100,
        choices=DEPENDENCY_TYPES,
        default='other'
    )
    description = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(source_team=models.F('target_team')),
                name='no_self_dependency'
            )
        ]

    def __str__(self):
        return f"{self.source_team} → {self.target_team} ({self.dependency_type})"
    


# ─────────────────────────────────────────
#  CONTACT CHANNEL
# ─────────────────────────────────────────
class ContactChannel(models.Model):
    CHANNEL_TYPES = [
        ('slack', 'Slack'),
        ('email', 'Email'),
        ('teams', 'Microsoft Teams'),
        ('other', 'Other'),
    ]
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='contact_channels'
    )
    channel_type = models.CharField(max_length=50, choices=CHANNEL_TYPES)
    channel_value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.team.team_name} - {self.channel_type}"
    


# ─────────────────────────────────────────
#  TEAM CHANNEL
# ─────────────────────────────────────────
class TeamChannel(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='channels'
    )
    channel_name = models.CharField(max_length=100)
    platform = models.CharField(max_length=50)
    channel_link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.team.team_name} - {self.channel_name}"


# ─────────────────────────────────────────
#  REPOSITORY
# ─────────────────────────────────────────
class Repository(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='repositories'
    )
    repo_name = models.CharField(max_length=200)
    repo_url = models.URLField(blank=True)
    repo_description = models.TextField(blank=True)

    def __str__(self):
        return self.repo_name


# ─────────────────────────────────────────
#  MESSAGE
# ─────────────────────────────────────────
class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Sent')

    def __str__(self):
        return self.subject


# ─────────────────────────────────────────
#  MEETING
# ─────────────────────────────────────────
class Meeting(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='meetings'
    )
    scheduled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='scheduled_meetings'
    )
    date_time = models.DateTimeField()
    platform = models.CharField(max_length=100)
    meeting_link = models.URLField(blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='Scheduled')

    def __str__(self):
        return f"{self.team.team_name} meeting - {self.date_time}"


# ─────────────────────────────────────────
#  AUDIT LOG
# ─────────────────────────────────────────
class AuditLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )
    entity_name = models.CharField(max_length=200)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.entity_name} - {self.action} at {self.timestamp}"
