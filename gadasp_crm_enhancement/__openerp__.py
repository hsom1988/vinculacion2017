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
                    'crm',
    ],
    'update_xml'  :[
                    #SEGURIDAD
                    #'security/ir.model.access.csv',
                    #Views
                    'views/crm_lead_view.xml',
                    'views/res_partner_view.xml',
    ],
    'auto_install': False,
    'installable' : True
}
