{
    "name": "Odoo_AI_App",
    "version": "1.0",
    "author": "phucnguyen12328",
    "description": """
        Odoo_AI_App show available properties
    """,
    "category" : "Tool",
    "depends": ["base","website","mail"],
    'qweb': [
    ],
    "data": [    
        'views/res_config_settings_views.xml',
        'data/openai_odoo_connector_data.xml',
        'data/openai_completion_data.xml',
    ],
    'uninstall_hook': 'uninstall_hook',
    'install_hook': 'install_hook',
    'images': ['static/description/module_image.png'],
    'auto_install': False,
    'application': True,
    'installable': True,
    'price': 0,
    'currency': 'EUR',
    "license":   "LGPL-3"
}