# Author: Akram Hassan
# Student ID: w2116400

from io import BytesIO

import xlsxwriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


# Get a readable department head name for the reports.
def get_department_head_name(department):
    if department.department_head:
        return department.department_head.get_full_name() or department.department_head.username
    return "Unassigned"


# Build the Excel export for the reports page.
def build_excel_export(snapshot):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    # Reusable formatting for the workbook.
    title_format = workbook.add_format({'bold': True, 'font_size': 16})
    header_format = workbook.add_format({'bold': True, 'bg_color': '#DCE8F6', 'border': 1})
    cell_format = workbook.add_format({'text_wrap': True, 'border': 1})

    # Summary sheet with the main overall metrics.
    summary_sheet = workbook.add_worksheet('Summary')
    summary_sheet.write('A1', 'Sky Engineering Portal Report Summary', title_format)
    summary_sheet.write_row('A3', ['Metric', 'Value'], header_format)

    row = 3
    for key, value in snapshot['stats'].items():
        summary_sheet.write_row(row, 0, [key.replace('_', ' ').title(), value], cell_format)
        row += 1

    summary_sheet.set_column('A:A', 28)
    summary_sheet.set_column('B:B', 16)

    # Department sheet showing team counts.
    count_sheet = workbook.add_worksheet('Team Counts')
    count_sheet.write('A1', 'Teams by Department', title_format)
    count_sheet.write_row('A3', ['Department', 'Department Head', 'Team Count'], header_format)

    row = 3
    for department in snapshot['team_count_by_department']:
        count_sheet.write_row(
            row,
            0,
            [
                department.department_name,
                get_department_head_name(department),
                department.team_count
            ],
            cell_format,
        )
        row += 1

    count_sheet.set_column('A:B', 24)
    count_sheet.set_column('C:C', 12)

    # Sheet for teams that do not have a manager assigned.
    missing_sheet = workbook.add_worksheet('Teams Without Managers')
    missing_sheet.write('A1', 'Teams Without Managers', title_format)
    missing_sheet.write_row('A3', ['Department', 'Team', 'Status'], header_format)

    row = 3
    teams_without_managers = list(snapshot['teams_without_managers'])

    if teams_without_managers:
        for team in teams_without_managers:
            missing_sheet.write_row(
                row,
                0,
                [
                    team.department.department_name if team.department else 'No department',
                    team.team_name,
                    'Active' if team.is_active else 'Inactive'
                ],
                cell_format,
            )
            row += 1
    else:
        missing_sheet.write('A4', 'No unmanaged teams found.', cell_format)

    missing_sheet.set_column('A:C', 24)

    # Finalise the file and return it as bytes.
    workbook.close()
    output.seek(0)
    return output.getvalue()


# Build the PDF export for the reports page.
def build_pdf_export(snapshot):
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4)
    styles = getSampleStyleSheet()

    # Opening content for the PDF.
    elements = [
        Paragraph('Sky Engineering Portal Reports', styles['Title']),
        Paragraph('Reports menu: PDF and Excel exports', styles['BodyText']),
        Spacer(1, 12),
        Paragraph('Summary Metrics', styles['Heading2']),
    ]

    # Summary metrics table.
    metric_rows = [['Metric', 'Value']]
    for key, value in snapshot['stats'].items():
        metric_rows.append([key.replace('_', ' ').title(), str(value)])

    elements.append(_styled_table(metric_rows, [260, 120]))
    elements.append(Spacer(1, 12))

    # Department team count table.
    elements.append(Paragraph('Team Count by Department', styles['Heading2']))

    department_rows = [['Department', 'Department Head', 'Team Count']]
    for department in snapshot['team_count_by_department']:
        department_rows.append([
            department.department_name,
            get_department_head_name(department),
            str(department.team_count)
        ])

    elements.append(_styled_table(department_rows, [170, 180, 90]))
    elements.append(Spacer(1, 12))

    # Missing manager table.
    elements.append(Paragraph('Teams Without Managers', styles['Heading2']))

    missing_rows = [['Department', 'Team', 'Status']]
    missing_teams = list(snapshot['teams_without_managers'])

    if missing_teams:
        for team in missing_teams:
            missing_rows.append([
                team.department.department_name if team.department else 'No department',
                team.team_name,
                'Active' if team.is_active else 'Inactive'
            ])
    else:
        missing_rows.append(['-', 'No unmanaged teams found.', '-'])

    elements.append(_styled_table(missing_rows, [150, 250, 90]))

    # Build the PDF and return it as bytes.
    doc.build(elements)
    output.seek(0)
    return output.getvalue()


# Apply a shared style to PDF tables.
def _styled_table(rows, column_widths):
    table = Table(rows, colWidths=column_widths, repeatRows=1)

    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DCE8F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#132238')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#9AB5D6')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FBFF')]),
        ])
    )

    return table
