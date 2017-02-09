# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source TRESCloud
#    Copyright (c) 2014-TRESCloud S.A. (<http://www.trescloud.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'states cities zones parishes of Ecuador',
    'version': '1.0',
    'category': 'sale',
    'depends': ['base',
                ],
    'author': 'TRESCLOUD Cia. Ltda.',
    'description': 
    """
    Resumen:
    Modulo que permite cargar datos de Provincias ciudades zonas y parroquias  
    del pais de Ecuador con sus respectivas vistas. 
         
                                                          

    Funciones:
    Carga provincias con sus respectivos codigos de provincia y nombres de provincias para el pais de Ecuador
    Carga ciudades o Cantones  dependiendo de su respectiva provincia y sus datos como codigo de la ciudad y nombre
    Carga las administraciones zonales definidas como zonas de la ciudad de quito con su codigo de zona y su nombre
    Carga las diferentes parroquias  que tiene una administración zonal con su codigo de parroquia y nombre de parroquia
    Genera las vistas de Ciudades, Zonas, Parroquias para su uso y crea sus diferentes menus  adicionados a libreta de direcciones 
    
    Authors: 
    Henry Granada
    TRESCLOUD Cia Ltda
    """,
    'website': 'http://www.trescloud.com',
    'data': [
    #Security
    'security/security.xml',
    'security/ir.model.access.csv',
    #vista form de modificación de campos para generar en orden  pasise provincias ciudades zonas  parroquias 
    'views/res_partner_view.xml',         
    #vistas form para poder adicionar ciudades, zonas, parroquias
    'views/res_city_view.xml',
    'views/res_zone_view.xml',
    'views/res_parish_view.xml',         
    #archivos csv de provincias, ciudades, zonas y parroquias del ecuador
    #===========================================================================
    'data/res.country.state.csv',
    'data/res.city.csv',
    'data/res.zone.csv',
    'data/res.parish.csv',
    #===========================================================================
    'security/security.xml',
    'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
