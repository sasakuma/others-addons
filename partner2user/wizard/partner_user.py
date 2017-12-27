# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CreateUser(models.TransientModel):
    _name = 'partner.user'
    _description = 'Create login from partner'

    @api.model
    def default_get(self, fields):
        res = super(CreateUser, self).default_get(fields)
        vals = []
        for aid in self._context.get('active_ids'):
            partner_id = self.env['res.partner'].browse(aid)
            vals.append((0, 0, {'partner_id': partner_id.id,
                                'login': partner_id.email}))
        res['user_data'] = vals
        return res

    user_data = fields.One2many('user.datas', inverse_name='rel_id')

    @api.multi
    def create_login(self):
        for data in self:
            for da in data.user_data:
                vals = {
                    'partner_id': da.partner_id.id,
                    'login': da.login,
                    'password': da.password,
                    'action_id': da.action_id.id,
                }
                user = self.env['res.users'].create(vals)
                da.role_ids.line_ids = [(0, 0, {
                    'user_id': user.id,
                })]


class CreateUserData(models.TransientModel):
    _name = 'user.datas'

    rel_id = fields.Many2one('partner.user')

    partner_id = fields.Many2one('res.partner', string='Partner')

    login = fields.Char('Login')

    password = fields.Char(string='Password')

    role_ids = fields.Many2one('res.users.role', string='Access Rule')

    action_id = fields.Many2one('ir.actions.actions', string='Initial Action')

    groups_id = fields.Many2many('res.groups', 'res_groups_users_rel',
                                 'uid', 'gid', string='Groups')
