{
    'name'        : 'Fleet enhancements',
    'version'     : '1.0',
    'category'    : 'Managing equipment and contracts',
    'author'      : 'TRESCLOUD CIA. LTDA.',
    'maintainer'  : 'TRESCLOUD CIA. LTDA.',
    'website'     : 'http://www.trescloud.com',        
    'description' : ''' 
                        Modulo que mejora esteticamente los modulos base para manejo de flota
                                              
                        Author: Santiago Orozco
                    ''',
    'depends'     :[
                    'base',
                    'document',
                    'crm',
                    'report_aeroo_ooo'
    ],
    'update_xml'  :[
                    # Seguridad
                    'security/ir.model.access.csv',
                    # Vistas
                    'views/crm_lead_view.xml',
                    'views/res_partner_view.xml',
                    'views/res_company_view.xml',
                    # Data
                    'data/crm_email_data.xml',
                    'data/crm_sequence.xml',
                    # Reportes
                    'reports/report_ticket_data.xml',
    ],
    'auto_install': False,
    'installable' : True
}
