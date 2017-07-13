# -*- coding:utf-8 -*-

from odoo import models, fields


class HrContract(models.Model):

    _inherit = 'hr.contract'

    mark_color = fields.Boolean('Mark name with color')
