from odoo import api, fields, models


class AnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    department_id = fields.Many2one('hr.department',
                                    string='Department')
