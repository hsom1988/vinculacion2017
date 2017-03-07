# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
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

from openerp.addons.base_status.base_stage import base_stage
import crm
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.osv import fields, osv, orm
import time
from openerp import SUPERUSER_ID
from openerp import tools
from openerp.tools.translate import _
from openerp.tools import html2plaintext

from base.res.res_partner import format_address

AVAILABLE_STATES = [
    ('draft', u'Recepción'),
    ('open', u'Análisis y reasignación'),
    ('president', 'Presidencia'),
    ('draft_post','Borrador'),
    ('send_post', 'Enviados'),
    ('received_post', 'Recibidos'),
    ('done', 'Respuesta'),
    ('cancel', 'Negado'),
]

class crm_lead(osv.osv):
    """ CRM Lead Case """
    _inherit = "crm.lead"
    
    def create(self, cr, uid, vals, context=None):
        vals = vals or {}
        view_id = self.pool.get('ir.model.data').get_object_reference(cr, 
                                                                      uid, 'gadasp_crm_enhancement', 
                                                                      'seq_ticket_crm_lead')[1]
        vals['name'] = self.pool.get('ir.sequence').next_by_id(cr, uid, view_id) or '/'
        return super(crm_lead,self).create(cr, uid, vals, context)
    
    def case_secretary(self, cr, uid, ids, context=None):
        """ Mark the case as won: state=done and probability=100 """
        for lead in self.browse(cr, uid, ids):
            lead.write({'state': 'open'})
        return True
    
    def case_president(self, cr, uid, ids, context=None):
        """ Mark the case as won: state=done and probability=100 """
        for lead in self.browse(cr, uid, ids):
            lead.write({'state': 'president'})
        return True
    
    def case_denied(self, cr, uid, ids, context=None):
        """ Mark the case as won: state=done and probability=100 """
        for lead in self.browse(cr, uid, ids):
            lead.write({'state': 'cancel'})
        return True
    
    def case_approved(self, cr, uid, ids, context=None):
        """ Mark the case as won: state=done and probability=100 """
        for lead in self.browse(cr, uid, ids):
            view_id = self.pool.get('ir.model.data').get_object_reference(cr, 
                                                                      uid, 'gadasp_crm_enhancement', 
                                                                      'seq_post_crm_lead')[1]
            post_name = self.pool.get('ir.sequence').next_by_id(cr, uid, view_id) or '/'
            lead.write({'state': 'draft_post',
                        'oficio_number': post_name + ' BORRADOR'})
        return True
    
    def case_send(self, cr, uid, ids, context=None):
        """ Mark the case as won: state=done and probability=100 """
        for lead in self.browse(cr, uid, ids):
            lead.write({'state': 'send_post',
                        'oficio_number': lead.oficio_number[:9]})
        return True
    
    def case_received(self, cr, uid, ids, context=None):
        """ Mark the case as won: state=done and probability=100 """
        for lead in self.browse(cr, uid, ids):
            lead.write({'state': 'received_post'})
        return True
    
    def case_ended(self, cr, uid, ids, context=None):
        """ Mark the case as won: state=done and probability=100 """
        for lead in self.browse(cr, uid, ids):
            lead.write({'state': 'done'})
        return True
    
    def action_send_response(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'sale', 'email_template_edi_crm_lead')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False 
        ctx = dict(context)
        ctx.update({
            'default_model': 'crm.lead',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        
    def _get_days_due(self, cr, uid, context=None):
        '''
        Este método se encarga de obtener los días de validez de la proforma definidos en la compañía
        :param cr: Cursor estándar de base de datos PostgreSQL
        :param uid: ID del usuario actual
        :param context: Diccionario de datos de contexto adicional
        '''
        if context is None:
            context = {}
        res_user_obj = self.pool.get('res.users')
        days_of_valid_proforma = 8
        for user in res_user_obj.browse(cr, uid, [uid], context=context):
            days_of_valid_proforma = user.company_id.days_due
        return days_of_valid_proforma

    _columns = {
        'name': fields.char("No. Tramite"),
        'description': fields.text('Notes', states={'done': [('readonly', True)]}),
        'oficio_number': fields.char('Oficio Nro.', states={'done': [('readonly', True)]}),
        'oficio_respuesta': fields.char('Nro. Oficio Resp.', states={'done': [('readonly', True)]}),
        'additional_information': fields.text('Observaciones', states={'done': [('readonly', True)]}),
        'date_open': fields.datetime('Fecha de recepcion',states={'done': [('readonly', True)]}),
        'date_max_resp': fields.datetime('Fecha max. de respuesta',states={'done': [('readonly', True)]}),
        'relevant': fields.boolean('Es Relevante?',states={'done': [('readonly', True)]}),
        'phonecall_ids': fields.one2many('crm.phonecall', 'opportunity_id', u'LLamadas Telefónicas',
                                         states={'done': [('readonly', True)]}),
        'external': fields.boolean('Es Externo?', states={'done': [('readonly', True)]}),
        'area_id': fields.many2one('res.area', u'Área', states={'done': [('readonly', True)]}),
        'urgente': fields.boolean('Urgente', states={'done': [('readonly', True)]}),
        'state': fields.selection(AVAILABLE_STATES, "Status", readonly=True, select=True,
                help='The Status is set to \'Draft\', when a case is created.'
                ' If the case is in progress the Status is set to \'Open\'. '
                'When the case is over, the Status is set to \'Done\'. If the'
                ' case needs to be reviewed then the Status is  set to \'Pending\'.'),
        'asunto': fields.char('Asunto',states={'done': [('readonly', True)]}),
        'header': fields.text('Cabecera', states={'done': [('readonly', True)]}),
        'body': fields.text('Cuerpo', states={'done': [('readonly', True)]}),
        'footer': fields.text(u'Pie de Página', states={'done': [('readonly', True)]}),
    }
    
    _defaults = {
        'date_open': lambda *a:datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date_max_resp': lambda self, cr, uid, context={}: (datetime.now()+\
                         relativedelta(days=self._get_days_due(cr, uid, context))).\
                         strftime('%Y-%m-%d %H:%M:%S'),
        'state': 'draft',
        }

crm_lead()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: