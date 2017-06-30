# -*- coding: utf-8 -*-

{
    'name': 'Postit Systray Menu',
    'version': '10.0.1.0.0',
    'author': 'MultidadosTI',
    'maintainer': 'MultidadosTI',
    'website': 'www.multidadosti.com.br',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'summary': 'This Module creates a widget in navbar that links to postit '
               'views.',
    'contributors': [
        'Rodrigo Ferreira <rodrigosferreira91@gmail.com>',
    ],
    'depends': [
        'web',
        'prisme_postit',
    ],
    'data': [
        'views/web_templates.xml',
    ],
    'qweb': [
        'static/src/xml/systray.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
