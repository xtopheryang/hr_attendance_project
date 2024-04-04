# -*- coding: utf-8 -*-
{
    'name': 'Attendance with Project and Task Selection',
    'version': '16.0.0.0',
    'category': 'Attendance',
    'author': 'Christopher Yang',
    'summary': 'Attendance with Project and Task Selection',
    'description': """
    Attendance with Project and Task Selection
    """,
    'depends': [
        'hr_attendance',
        'project',
    ],
    'data': [
        'views/hr_attendance_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hr_attendance_project/static/src/js/attendance.js',
            'hr_attendance_project/static/src/xml/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
