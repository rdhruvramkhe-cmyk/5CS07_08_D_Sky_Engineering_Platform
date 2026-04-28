from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from teams.models import AuditLog

from .exporters import build_excel_export, build_pdf_export
from .services import build_reports_snapshot


def dashboard(request):
    snapshot = build_reports_snapshot()
    return render(request, 'reports/dashboard.html', snapshot)


def export_excel(request):
    snapshot = build_reports_snapshot()
    payload = build_excel_export(snapshot)
    timestamp = timezone.now().strftime('%Y%m%d_%H%M')
    AuditLog.objects.create(
        action='reports_export_excel',
        details='Generated Excel report export from the Reports menu.',
    )
    response = HttpResponse(
        payload,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="sky_reports_{timestamp}.xlsx"'
    return response


def export_pdf(request):
    snapshot = build_reports_snapshot()
    payload = build_pdf_export(snapshot)
    timestamp = timezone.now().strftime('%Y%m%d_%H%M')
    AuditLog.objects.create(
        action='reports_export_pdf',
        details='Generated PDF report export from the Reports menu.',
    )
    response = HttpResponse(payload, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="sky_reports_{timestamp}.pdf"'
    return response
