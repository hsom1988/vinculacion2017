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
  
 
class res_parish(osv.osv):
     _name = "res.parish"   
     _columns = {
        'name': fields.char('Parish Name', size=40, required=True, 
                            help='Administrative divisions of parish.'),
        'code': fields.char('Parish Code', size=3,
            help='The parish code in max. three chars.', required=True),
        'zone_id': fields.many2one('res.zone', 'Zone', help='Select the associated area parishes',
            required=True),
        'city_id': fields.related(
                                  'zone_id', 
                                  'city_id', 
                                  type='many2one', 
                                  relation='res.city', 
                                  string="City",
                                  help='The city associated with the zone and parish', 
                                  readonly=True),
         # 'state_id': fields.related('state_id', 'city_id', type='many2one', relation='res.city', string=""),
         #======================================================================
        'active': fields.boolean('Active')
     }

     _defaults = {
         'active': True
     }
     
        # funcion unlink para  controlar que no se pueda elimiar una parroquia asociada  a un cliente 
     def unlink(self, cr, uid, ids, context=None):
            partner_ids = self.pool.get('res.partner').search(cr, uid, [('parish_id','=',ids[0])], context=context)
            if partner_ids:
                raise osv.except_osv(_('Invalid Action!'), _('To remove a parish must first disassociate the client related to parish.'))
            else:
                osv.osv.unlink(self, cr, uid, ids, context=context)
            return True
        
     # funcion que permite  controlar el duplicado de datos   
     def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context={}
        if not default:
            default = {}
        parish = self.read(cr, uid, id, ['name'], context=context)
        default = default.copy()
        default.update(name=_("%s (copy)") % (parish['name']))
        return super(res_parish, self).copy(cr, uid, id, default=default,
                    context=context)
     
      
res_parish()



  
   
  