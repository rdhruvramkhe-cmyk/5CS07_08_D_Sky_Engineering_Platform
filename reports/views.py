# Author: Akram Hassan
# Student ID: w2116400

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from teams.models import AuditLog

from .exporters import build_excel_export, build_pdf_export
from .services import build_reports_snapshot


# Display the main reports dashboard.
def dashboard(request):
    snapshot = build_reports_snapshot()
    return render(request, 'reports/dashboard.html', snapshot)


# Export the current report data as an Excel file.
def export_excel(request):
    snapshot = build_reports_snapshot()
    payload = build_excel_export(snapshot)
    timestamp = timezone.now().strftime('%Y%m%d_%H%M')

    # Record the export in the audit log.
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


# Export the current report data as a PDF file.
def export_pdf(request):
    snapshot = build_reports_snapshot()
    payload = build_pdf_export(snapshot)
    timestamp = timezone.now().strftime('%Y%m%d_%H%M')

    # Record the export in the audit log.
    AuditLog.objects.create(
        action='reports_export_pdf',
        details='Generated PDF report export from the Reports menu.',
    )

    response = HttpResponse(payload, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="sky_reports_{timestamp}.pdf"'
    return response
