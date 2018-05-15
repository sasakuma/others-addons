{
    'name': 'Base Analytic Department Categorization',
    'version': '11.0.1.0.0',
    'author': 'Camptocamp, Daniel Reis, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'category': 'Generic Modules/Projects & Services',
    'website': 'https://github.com/OCA/account-analytic',
    'depends': [
        'analytic',
        'hr',
    ],
    'data': [
        'views/analytic.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
