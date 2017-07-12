# -*- coding: utf-8 -*-
{
    'name': 'CKEditor Widget Alpha',
    'summary': 'CKEditor Widget',
    'description': 'CKEditor Widget'
                   ' Based on CKEditor 4.6 `Docs in CKEditor'
                   ' <http://robinherbots.github.io/Inputmask/>`_.',
    'author': "Gilvan Leal",
    'website': "https://gilvanleal.github.io/odoowidgets/",
    'category': 'Extra Tools',
    'version': '0.1',
    'depends': [
        'web',
    ],
    "data": [
        'views/assets_templates.xml',
    ],
    "qweb": [
        'static/src/xml/editor.xml',
    ],
    'images': [
        'static/description/main_screenshot.png',
    ],
    'installable': True,
}
