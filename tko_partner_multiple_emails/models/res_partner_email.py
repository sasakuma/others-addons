# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    ThinkOpen Solutions Brasil
#    Copyright (C) Thinkopen Solutions <http://www.tkobr.com>.
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

from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)


class ResPartnerEmail(models.Model):
    _name = 'res.partner.email'
    _rec_name = 'email'

    MAIL_TYPE = [
        ('invoice', u'Nota Fiscal'),
        ('billet', u'Boleto'),
        ('invoice-billet', u'Nota Fiscal/Boleto'),
        ('notify-invoice', u'Notificação de Nota Fiscal'),
        ('notify-billet', u'Notificação de Boleto'),
    ]

    email = fields.Char('Email')
    partner_id = fields.Many2one('res.partner', u'Partner')
    is_main = fields.Boolean('Is Main', help="Main /Celular", default=False)
    mail_type = fields.Selection(string='Tipo',
                                 selection=MAIL_TYPE,
                                 required=True)

    @api.multi
    def set_main_email(self):
        for record in self:
            email_ids = self.search(
                [('partner_id', '=', record.partner_id.id)])
            email_ids.write({'is_main': False})
            vals = {
                'is_main': 't',
                'email': record.email,
            }
            record.partner_id.write(vals)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
