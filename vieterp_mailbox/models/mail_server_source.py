# -*- coding: utf-8 -*-
from odoo import models


class vieterp_mail_server_source(models.Model):
    _inherit = 'fetchmail.server'
    _name = 'mail.server.source'
