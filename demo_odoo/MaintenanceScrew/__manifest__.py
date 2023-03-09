# -*- coding: utf-8 -*-
{
    'name': "Maintenance Screw",

    'summary': """
        Maintenance App """,

    'description': """
        Application to maintenance machine
    """,

    'author': "Quoc Duong & Hoang Sang ",
    'website': "Updating",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'security/employee_security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/views_transientmodel.xml',
        'views/action_smart_button.xml',
        'views/views_machine.xml',
        'views/views_component.xml',
        'views/views_maintenance.xml',
        'views/views_factory.xml',
        'views/views_machine_location.xml',
        'views/views_warehouse.xml',
        'views/views_component_warehouse.xml',
        'views/views_import.xml',
        'views/views_export.xml',
        'views/views_model.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
