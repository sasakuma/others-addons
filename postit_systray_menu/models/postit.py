# -*- coding: utf-8 -*-

from odoo import models


class Postit(models.Model):
    _inherit = 'prisme.postit'

    def get_id_menu(self):
        return self.env.ref('prisme_postit.menu_prisme_postit_base')
