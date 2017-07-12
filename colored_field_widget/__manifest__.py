# -*- coding:utf-8 -*-
{
    'name': 'Custom colored widgets',
    'version': '10.0.1.0.0',
    'summary': 'Some custom widgets',
    'category': 'Tools',
    'author': 'KIT-XXI',
    'website': "http://kit-xxi.com.ua/",
    'description':
        """
Custom colored widgets
======================

A collection of custom widgets:
- Colored ListView field
- Colored ListView boolean field
        """,
    'data': [
        "views/custom_widget.xml"
    ],
    'depends': [
        'base',
        'web',
    ],
    'qweb': [
        'static/src/xml/template_update.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
