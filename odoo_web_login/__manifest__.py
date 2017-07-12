# -*- encoding: utf-8 -*-

{
    'name': 'Odoo Web Login Screen',
    'summary': 'The new configurable Odoo Web Login Screen',
    'version': '10.0.1.0',
    'category': 'Website',
    'author': "binhnguyenxuan (www.xubi.me)",
    'website': 'http://www.xubi.me',
    'license': 'AGPL-3',
    'depends': [
    ],
    'data': [
        'data/ir_config_parameter.xml',
        'views/webclient_templates.xml',
        'views/website_templates.xml',
    ],
    'qweb': [
    ],
    'installable': False,
    'application': True,
}
