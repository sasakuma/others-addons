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
    ],
    'data': [
        'views/postit_view.xml',
        'views/postit_workflow.xml',

    ],
    'demo': [

    ],
    'test': [
    ],
    'init_xml': [
        'data/init_scheduler.xml',

    ],
    'update_xml': [
        'security/ir.model.access.csv',
    ],
    'css': [
        'static/src/css/note.css',
    ],
    'images': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
