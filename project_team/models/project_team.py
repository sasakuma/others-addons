# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class CrmTeamInherit(models.Model):

    _inherit = 'crm.team'

    type_team = fields.Selection([('sale', 'Sale'),
                                  ('project', 'Project')],
                                 string="Type", default="sale")

    team_members = fields.Many2many('res.users', string='Project Members',
                                    help="""Project's members are users who
                                     can have an access to the tasks related
                                     to this project.""")

    @api.model
    def create(self, values):
        if 'team_members' not in values:
            values['team_members'] = [(4, values['user_id'])]
        else:
            values['team_members'][0][2].append(values['user_id'])

        return super(CrmTeamInherit, self).create(values)

    @api.multi
    def write(self, values):

        if 'user_id' not in values and self.user_id:
            values['user_id'] = self.user_id.id

        if 'user_id' in values:
            if 'team_members' not in values:
                values['team_members'] = [(4, values['user_id'])]
            else:
                values['team_members'][0][2].append(values['user_id'])

        return super(CrmTeamInherit, self).write(values)


class ProjectProject(models.Model):

    _inherit = 'project.project'

    team_id = fields.Many2one('crm.team', string="Project Team",
                              domain=[('type_team', '=', 'project')])

    members = fields.Many2many('res.users', string='Project Members',
                               related='team_id.team_members',
                               help="""Project's members are users who can
                               have an access to the tasks related to this
                               project.""")

    # @api.onchange('team_id')
    # def get_team_members(self):
    #     self.members = [(6, 0, [rec.id for rec in self.team_id.team_members])]
