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
        'city_id': fields.many2one('res.city','City',
            required=True),
           }

    
class res_city(osv.osv):
     _name = "res.city"   
     _columns = {
                 
        'name': fields.char('City Name', size=40, required=True, 
                            help='Administrative divisions of a State.'),
        'code': fields.char('City Code', size=3,
            help='The city code in max. three chars.', required=True),
        'state_id': fields.many2one('res.country.state', 'State',
            required=True)
          
    }
     
class res_parish(osv.osv):
     _name = "res.parish"   
     _columns = {
        'name': fields.char('Parish Name', size=40, required=True, 
                            help='Administrative divisions of state.'),
        'code': fields.char('Parish Code', size=3,
            help='The city code in max. three chars.', required=True),
        'zone_id': fields.many2one('res.zone', 'Zone',
            required=True),
    }
  

  
class res_country_state(osv.osv):
     _inherit = "res.country.state"
     _name = "res.country.state"   
     _columns = {
        'state_ids': fields.many2one('res.city', 'state_id','City',
            required=True),
                 }
    

     
ADDRESS_FIELDS = ('street', 'street2', 'zip', 'parish_id', 'zone_id', 'city_id', 'city', 'state_id', 'country_id')
class res_partner(osv.osv):
    _description = 'information personal credits'
    _inherit="res.partner"
    _columns={
              'city_id': fields.many2one('res.city', 'City', required=False),
              'zone_id': fields.many2one('res.zone','Zone',required=False),
              'parish_id': fields.many2one('res.parish','Parish', required=False ),
              }
    
    def onchange_country(self, cr, uid, ids, country_id, context=None):
        if country_id:
            return {'value':{'state_id':'','city_id':'','city':'','zone_id':'','parish_id':'','zip':''}}
        return {}

    def onchange_state(self, cr, uid, ids, state_id, context=None):
        if state_id:
            return {'value':{'city_id':'','city':'','zone_id':'','parish_id':'','zip':''}}
        return {}
    
    def onchange_city(self, cr, uid, ids, city_id, context=None):
        resultado = ''
        if context is None:
             context={}
        if city_id:
             city_name = self.pool.get('res.city').browse(cr, uid, city_id, context=context)
             resultado= city_name.name
             
             return {'value':{'zone_id':'', 'parish_id':'', 'zip':'', 'city':resultado}}
        return {}

    def onchange_zone(self, cr, uid, ids, zone_id, context=None):
        if zone_id:
            return {'value':{'parish_id': '','zip':''}}
        return {}
   
       
    def onchange_parish(self, cr, uid, ids, parish_id, context=None):
        if parish_id:
            return {'value':{'zip':''}}
        return {}
    
    def _address_fields(self, cr, uid, context=None):
        """ Returns the list of address fields that are synced from the parent
        when the `use_parent_address` flag is set. """
        return list(ADDRESS_FIELDS)
    
    
res_partner()



  
   
  