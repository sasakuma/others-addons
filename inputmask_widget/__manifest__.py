# -*- coding: utf-8 -*-
{
    'name': "Inputmask Widget",
    'summary': """A Widget to make masks on form fields""",
    'author': "Gilvan Leal",
    'website': "https://gilvanleal.github.io/odoowidgets/",
    'category': 'Extra Tools',
    'version': '10.0.1.0.0',
    'depends': [
        'web',
    ],
    "data": [
        'views/assets_templates.xml',
    ],
    "qweb": [
        'static/src/xml/mask.xml',
    ],
    'images': [
        'static/description/main_screenshot.png',
    ],
    'installable': False,
}
