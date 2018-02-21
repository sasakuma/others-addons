{
    'name': 'Postit',
    'version': '11.0.1.0.0',
    'author': 'Prisme',
    'maintainer': 'MultidadosTI',
    'website': 'www.multidadosti.com.br',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'summary': 'This Module creates a widget in navbar that links to postit '
               'views.',
    'contributors': [
        'Michell Stuttgart <michellstut@gmail.com>',
        'Rodrigo Ferreira <rodrigosferreira91@gmail.com>',
    ],
    'depends': [
        'mail',
    ],
    'data': [
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
        'views/postit_view.xml',
    ],
    'css': [
        'static/src/css/note.css',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
