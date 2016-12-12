# -*- coding: utf-8 -*-
{
    'license': 'LGPL-3',
    'name': "Document Manage",
    'summary': "manage related document attachments",
    'description': """
    """,
    'author': "renjie <i@renjie.me>",
    'website': "http://renjie.me",
    'category': 'Document Management',
    'version': '1.1',
    'depends': ['document'],
    'data': [
        'views/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/base.xml",
    ],
    'images': [
        'static/description/main_screenshot.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}