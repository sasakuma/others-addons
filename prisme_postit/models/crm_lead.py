# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    postit_id = fields.Many2one(comodel_name='prisme.postit', string='Postit')
    postit_count = fields.Integer("Postit",
                                  compute='_compute_postit_count')

    @api.multi
    def _compute_postit_count(self):
        for lead in self:
            lead.postit_count = self.env['prisme.postit'].search_count(
                [('id', '=', lead.postit_id.id)])

    @api.multi
    def redirect_postit(self):
        action = self.env['ir.actions.act_window'].for_xml_id(
            'prisme_postit', 'action_prisme_postit')

        action['domain'] = [('id', '=', self.postit_id.id)]
        action['view_id'] = self.env.ref(
            'prisme_postit.view_prisme_postit_form').id
        action['view_ids'] = [action['view_id']]
        action['view_mode'] = 'form'
        action['view_type'] = 'form'

        return action
