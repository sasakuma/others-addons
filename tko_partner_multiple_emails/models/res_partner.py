
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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    email_ids = fields.One2many('res.partner.email',
                                'partner_id',
                                string=u'Emails')

    @api.multi
    def get_email_list(self, types=[]):
        """Verifica emails no cadastro do partner e retorna uma string contendo
         os emails do tipo especificado em types.

        :param types: lista dos tipos de emails que deseja serem retornados
        :return: string com emails do tipo definido em types separados por ','
        """
        emails = self.email_ids.filtered(lambda r: r.mail_type in types)
        emails = emails.mapped('email')
        return ','.join(emails)
