# -*- coding: utf-8 -*-
from odoo import fields, models


class PrismePostItTag(models.Model):
    _name = 'prisme.postit.tag'
    _description = 'Postit Tag'
    name = fields.Char(string='Tag name', required=True)
