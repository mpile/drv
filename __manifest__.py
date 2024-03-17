{
    'name': "Auto škola",

    'summary': """
        Modul za administrativno poslovanje auto-škola.""",

    'description': """
        Modul za administrativno poslovanje auto-škola
    """,

    'author': "Art-Info, doo",
    "application" : True,
    'sequence': -111,
    "license" : 'LGPL-3',    
    'website': "https://www.art-info.rs",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','web'], 
    # always loaded
    'data': [  
        'data/drv_racun_sequence.xml',                 
        'security/ir.model.access.csv',  
        'reports/ti_layout.xml',                     
        'reports/land_format.xml',   
        'reports/ti_report.xml',  
        'reports/pi_report.xml',      
        'reports/drv_svjed_report.xml',     
        'views/drv_sql_ti_view.xml',   
        'views/drv_sql_pi_view.xml',                          
        'views/drv_meni.xml',                                     
        'views/drv_res_candidate.xml',
        'views/drv_config_settings.xml',         
        'views/drv_cena_view.xml',
        'views/drv_ti_view.xml',  
        'views/drv_ti_line_view.xml',  
        'views/drv_pi_line_view.xml',              
        'views/drv_pi_view.xml',
        'views/drv_racuni_view.xml',
        'views/drv_racuni_line_view.xml',
        'views/drv_instruct_view.xml',
        'views/drv_sql_racun_view.xml'                                                                                                                                               
    ],
    # only loaded in demonstration mode    
}