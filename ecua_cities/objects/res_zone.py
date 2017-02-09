# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

import datetime
from lxml import etree
import math
import pytz
import re

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
  
 
class res_zone(osv.osv):
     _name = "res.zone"   
     _columns = {
        'name': fields.char('Zone Name', size=40, required=True,
                            help='Administrative divisions of the city.'),
        'code': fields.char('Zone Code', size=3,
            help='The zone code in max. three chars.', required=True),
        'city_id': fields.many2one('res.city','City', help='Select the city associated with areas ejm: City Quito Zone Adm. Quitumbe  ',
            required=True),
        'active': fields.boolean('Active')
     }

     _defaults = {
         'active': True
     }
     
     #==========================================================================
     # def zone_city(self, cr, uid, ids, zone_id, context=None):
     #     '''
     #     Funcion que permite buscar la ciudad a la que pertenece una zona
     #     '''
     # 
     #     if zone_id:
     #         zone_id = self.pool.get('res.zone').browse(cr, uid, zone_id, context).city_id.id
     #         return {'value':{'city_id'}}
     #     return {}
     #==========================================================================
     
        # funcion unlink para  controlar que no se pueda elimiar una zona asociada  a un cliente 
     def unlink(self, cr, uid, ids, context=None):
            partner_ids = self.pool.get('res.partner').search(cr, uid, [('zone_id','=',ids[0])], context=context)
            parish_ids= self.pool.get('res.parish').search(cr, uid, [('zone_id','=',ids[0])], context=context)
            
            if partner_ids or parish_ids:
                raise osv.except_osv(_('Invalid Action!'), _('To remove a zone must first disassociate the client related to zone or parishes.'))
            else:
                osv.osv.unlink(self, cr, uid, ids, context=context)
            return True
        
     # funcion que permite  controlar el duplicado de datos   
     def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context={}
        if not default:
            default = {}
        zone = self.read(cr, uid, id, ['name'], context=context)
        default = default.copy()
        default.update(name=_("%s (copy)") % (zone['name']))
        return super(res_zone, self).copy(cr, uid, id, default=default,
                    context=context)
      
res_zone()



  
   
  