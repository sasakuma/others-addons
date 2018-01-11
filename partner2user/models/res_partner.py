# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    show_create_user = fields.Boolean(string='Show Create User ?',
                                      compute='_compute_show_create_user')

    def _compute_show_create_user(self):

        for record in self:
            user = self.env['res.users'].search(
                [('partner_id', '=', record.id)])
            if user:
                record.show_create_user = False
            else:
                record.show_create_user = True
