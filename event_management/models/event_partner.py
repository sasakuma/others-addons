from odoo import models, fields, _


class ResPartner(models.Model):
    _name = 'event.partner'

    confirmed = fields.Boolean(string="Confirmed")

    partner_ids = fields.Many2one('res.partner')

    event_management_id = fields.Many2one('event.management', string="Event")
