{
    'name': "Partner to User",
    'version':'11.0.1.0.0',
    'summary': """
        Create a Login/User from a partner""",

    'description': """
        Long description of module's purpose
    """,
    'license': 'AGPL-3',
    'author': "KABEER KB",
    'website': "",
    'category': 'base',
    #'price':8,
    #'currency':'EUR',

    # any module necessary for this one to work correctly
    'depends': [
        'base_user_role',
    ],

    # always loaded
    'data': [

        'wizard/user_view.xml',
        'views/partner_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'application': False,

}
