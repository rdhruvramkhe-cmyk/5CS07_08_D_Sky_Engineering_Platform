from django.contrib import admin

from .models import AuditLog, ContactChannel, Department, Repository, Team, TeamDependency, TeamMember


class RepositoryInline(admin.TabularInline):
    model = Repository
    extra = 0


class ContactChannelInline(admin.TabularInline):
    model = ContactChannel
    extra = 0


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_name', 'specialization')
    search_fields = ('name', 'head_name')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'team_leader_name', 'jira_project_name')
    list_filter = ('department',)
    search_fields = ('name', 'team_leader_name', 'jira_project_name')
    inlines = [RepositoryInline, ContactChannelInline, TeamMemberInline]


@admin.register(TeamDependency)
class TeamDependencyAdmin(admin.ModelAdmin):
    list_display = ('source_team', 'target_team', 'dependency_type')
    search_fields = ('source_team__name', 'target_team__name', 'dependency_type')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'created_at')
    search_fields = ('action', 'details')


admin.site.register(Repository)
admin.site.register(ContactChannel)
admin.site.register(TeamMember)
