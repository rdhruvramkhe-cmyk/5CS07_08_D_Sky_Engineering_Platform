# Author: Akram Hassan
# Student ID: w2116400

from django.test import TestCase
from django.urls import reverse

from directory.models import ContactChannel, Department, Repository, Team, TeamDependency


class ReportsViewTests(TestCase):
    # Set up sample data used by the report tests.
    def setUp(self):
        self.department = Department.objects.create(name='xTV_Web', head_name='Sebastian Holt')

        self.managed_team = Team.objects.create(
            name='Code Warriors',
            department=self.department,
            team_leader_name='Olivia Carter',
            jira_project_name='Client Lightning Xtv',
        )

        self.unmanaged_team = Team.objects.create(
            name='Unassigned Incidents',
            department=self.department,
            team_leader_name='',
            jira_project_name='Incident Triage',
        )

        Repository.objects.create(
            team=self.managed_team,
            name='Code Warriors codebase',
            url='https://tiny.cc/x9b4t',
        )

        ContactChannel.objects.create(
            team=self.managed_team,
            channel_type=ContactChannel.ChannelType.SLACK,
            label='Slack channel 1',
            value='#code-warriors',
        )

        TeamDependency.objects.create(
            source_team=self.managed_team,
            target_team=self.unmanaged_team,
            dependency_type='Incident Support',
        )

    # Check that the dashboard loads and shows key report content.
    def test_dashboard_renders_summary_and_missing_manager_report(self):
        response = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student 5 Report Centre')
        self.assertContains(response, 'Unassigned Incidents')
        self.assertContains(response, 'Total Teams')

    # Check that the Excel export returns a valid .xlsx response.
    def test_excel_export_returns_xlsx_file(self):
        response = self.client.get(reverse('reports:export_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        self.assertTrue(response.content.startswith(b'PK'))

    # Check that the PDF export returns a valid PDF response.
    def test_pdf_export_returns_pdf_file(self):
        response = self.client.get(reverse('reports:export_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))
