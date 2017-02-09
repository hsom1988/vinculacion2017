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
  
 
class res_city(osv.osv):
     _name = "res.city"   
     _columns = {
        'name': fields.char('City Name', size=40, required=False, 
                            help='Administrative divisions of a Cities.'),
        'code': fields.char('City Code', size=3,
            help='The city code in max. three chars.', required=True),
        'state_id': fields.many2one('res.country.state', 'State', help='Select the state associated to the cities ejm: State Pichincha City Quito ',
            required=True),
        'active': fields.boolean('Active')
     }

     _defaults = {
         'active': True
     }
     
      # funcion unlink para  controlar que no se pueda elimiar una ciudad asociada  a un cliente o a una zona
     def unlink(self, cr, uid, ids, context=None):
            partner_ids = self.pool.get('res.partner').search(cr, uid, [('city_id','=',ids[0])], context=context)
            zone_ids= self.pool.get('res.zone').search(cr, uid, [('city_id','=',ids[0])], context=context)
            
            if partner_ids or zone_ids:
                raise osv.except_osv(_('Invalid Action!'), _('To remove a City must first disassociate the client related to City or Zones.'))
            else:
                osv.osv.unlink(self, cr, uid, ids, context=context)
            return True
        
     # funcion que permite  controlar el duplicado de datos   ciudades
     def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context={}
        if not default:
            default = {}
        city = self.read(cr, uid, id, ['name'], context=context)
        default = default.copy()
        default.update(name=_("%s (copy)") % (city['name']))
        return super(res_city, self).copy(cr, uid, id, default=default, context=context)
     
      
res_city()



  
   
  