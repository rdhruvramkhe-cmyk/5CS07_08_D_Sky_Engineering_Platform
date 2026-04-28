# Sky Engineering Portal
5COSC021W Coursework 2 — Group Project

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata teams/fixtures/teams_data.json
python manage.py createsuperuser
python manage.py runserver
```

## Test URLs
- `/` — Login
- `/teams/dashboard/` — Dashboard
- `/teams/` — Teams list
- `/organisation/` — Organisation structure
- `/departments/` — Departments
- `/sky/teams/<id>/` — Team detail (sky panel)
- `/reports/` — Reports
- `/admin/` — Admin panel

## Credentials
Create a superuser with `python manage.py createsuperuser`

## Apps
- `accounts` — Login, logout, signup
- `teams` — Teams, dashboard, meetings, shared models
- `sky` — Organisation & departments panel (Student 2 — Hisham Suleman)
- `reports` — Reports & exports (Student 5)
