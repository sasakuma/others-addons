# -*- coding: utf-8 -*-
{
    'name': 'Postit',
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
        'mail',
        'crm',
    ],
    'data': [
        'views/postit_view.xml',
        'views/crm_lead_views.xml',
        'views/postit_workflow.xml',
        'data/init_scheduler.xml',
        'security/ir.model.access.csv',
    ],
    'css': [
        'static/src/css/note.css',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
