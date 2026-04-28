from django.contrib import admin
from .models import (
    Department, Skill, Team, TeamMember, Repository,
    ContactChannel, TeamChannel, Dependency, Meeting,
    Message, AuditLog
)


class RepositoryInline(admin.TabularInline):
    model = Repository
    extra = 1


class ContactChannelInline(admin.TabularInline):
    model = ContactChannel
    extra = 1


class TeamChannelInline(admin.TabularInline):
    model = TeamChannel
    extra = 1


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'department', 'team_leader', 'is_active')
    search_fields = ('team_name', 'mission', 'description', 'department__department_name')
    list_filter = ('department', 'is_active', 'skills')
    filter_horizontal = ('skills',)
    inlines = [RepositoryInline, ContactChannelInline, TeamChannelInline, TeamMemberInline]


admin.site.register(Department)
admin.site.register(Skill)
admin.site.register(Dependency)
admin.site.register(Meeting)
admin.site.register(Message)
admin.site.register(AuditLog)