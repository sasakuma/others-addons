# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    postit_ids = fields.Many2many(comodel_name='prisme.postit',
                                  string='Postit')
    postit_count = fields.Integer("Postit",
                                  compute='_compute_postit_count')

    @api.multi
    def _compute_postit_count(self):
        self.postit_count = len(self.postit_ids)
        # for lead in self:
        #     lead.postit_count = self.env['prisme.postit'].search_count(
        #         [('postit_ids', '=', lead.postit_ids.id)])

    @api.multi
    def action_redirect_postit(self):
        action = self.env['ir.actions.act_window'].for_xml_id(
            'prisme_postit', 'action_prisme_postit')

        action['domain'] = [('id', 'in', self.postit_ids.ids)]
        action['view_id'] = self.env.ref(
            'prisme_postit.view_prisme_postit_form').id
        action['view_ids'] = [action['view_id']]
        action['view_mode'] = 'form'
        action['view_type'] = 'form'
        action['context'] = {'default_lead_ids': self.ids,
                             'default_partner_id': self.partner_id.id}

        return action
