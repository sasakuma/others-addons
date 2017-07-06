# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
from odoo import tools
from odoo import api, fields, models, _

AVAILABLE_PRIORITIES = [
    ('0', 'Muito Baixa'),
    ('1', 'Baixa'),
    ('2', 'Normal'),
    ('3', 'Alta'),
    ('4', 'Muito Alta')]


class PrismePostit(models.Model):
    """ Post It data """
    _name = 'prisme.postit'
    _description = 'Postit'
    _inherit = ['mail.thread']

    name = fields.Char(string="Name", required=True)
    names_users = fields.Char(string="Assigned to")
    description = fields.Text(required='True')
    assigned_by = fields.Many2one('res.users', string="Assigned by",
                                  default=lambda self: self._uid)
    assigned_to = fields.Many2many('res.users', 'prisme_postit_assignedto_rel',
                                   string="Assigned to",
                                   required=True)
    copy_to = fields.Many2many('res.users', 'prisme_postit_copyto_rel',
                               string="Copy to")
    partner_id = fields.Many2one('res.partner', string="Client")
    priority = fields.Selection(string="Priority",
                                selection=AVAILABLE_PRIORITIES,
                                default='0',
                                select=True)
    tags = fields.Many2many('prisme.postit.tag', string="Tags")
    days = fields.Many2many('prisme.postit.day', string="Days")
    date_start = fields.Date(string="Date start")
    date_end = fields.Date(string="Date end")
    expected_date = fields.Date(string="Expected Date")
    state = fields.Selection([('active', 'Non termine'),
                              ('in_process', 'En cours'), (
                                  'terminated', 'Termine'), ],
                             default='active')

    active = fields.Boolean(default=True)

    opportunity_count = fields.Integer("Opportunity",
                                       compute='_compute_opportunity_count')

    crm_lead_id = fields.Many2one(comodel_name='crm.lead')

    @api.model
    def action_in_process(self):
        self.state = 'in_process'
        self.date_start = fields.datetime.now()

    @api.model
    def action_close(self):
        self.state = 'terminated'
        self.date_end = fields.datetime.now()

    @api.model
    def action_active(self):
        return self.write({'state': 'active'})

    @api.model
    def scheduled_action(self, context=None):
        self._check_postit_dates()

    @api.model
    def _check_postit_dates(self):

        postits = self.search([('state', '!=', 'closed')])
        for p in postits:
            if p.state != "closed" and p.recall_date:
                recall_date = datetime.strptime(p.recall_date, "%Y-%m-%d")

                if recall_date <= datetime.now() and p.state in ["start",
                                                                 "in_process",
                                                                 "active"]:
                    weekday = p.days if p.days else []
                    for day in weekday:
                        if datetime.now().weekday() == day.nbr:
                            p._notify_recall(" en cours, echeance le ")

    @api.model
    def _notify_recall(self, message):
        subject = self._construct_subject(message)
        body = self._construct_body()

        ass_by = None
        ass_to_list = None
        copy_to_list = None
        if self.assigned_by:
            ass_by = self.assigned_by.email
        if self.assigned_to:
            ass_to_list = self.assigned_to
        if self.copy_to:
            copy_to_list = self.copy_to

        sender = 'Postit - OpenERP (' + self.env.cr.dbname + \
                 ') <system.openerp@prisme.ch>'

        if ass_by:
            # Sending e-mail to the user
            self._send_email(sender, ass_by, subject, body)
        if ass_to_list:
            for ass_to in ass_to_list:
                if not ass_to.email == ass_by:
                    self._send_email(sender, ass_to.email, subject, body)
        if copy_to_list:
            for copy_to in copy_to_list:
                if not copy_to == ass_by and not copy_to.email == ass_to.email:
                    self._send_email(sender, copy_to, subject, body)

    @api.model
    def _construct_subject(self, message):
        end_date_string = ""
        if self.date_end:
            end_date_string = "(" + self.date_end + ")"
        subject = "Postit (" + self.name + ")" + message + end_date_string
        return subject

    @api.model
    def _construct_body(self):

        body = "Rappel d'expiration de tache" + "\n"
        body = body + "-------------------------------\n\n"

        body = body + "Tache: " + self.name + "\n"

        if self.assigned_by:
            body = body + "Assigne par: " + self.assigned_by.name + "\n"
        if self.partner_id:
            body = body + "Client: " + self.partner_id.name + "\n"
        if self.date_start:
            body = body + "Date de debut: " + self.date_start + "\n"
        if self.date_end:
            body = body + "Date limite: " + self.date_end + "\n"
        if self.duration:
            body = body + "Duree: " + self.duration + "\n"
        if self.recall_date:
            body = body + "Date echeance Postit: " + self.recall_date + "\n\n"

        if self.assigned_to:
            for ass_to in self.assigned_to:
                body = body + "Assigne a: " + ass_to.name + "\n"
        if self.copy_to:
            for copy_to in self.copy_to:
                body = body + "Copie a: " + copy_to.name + "\n\n"
        if self.description:
            body = body + "Description: \n" + self.description + "\n\n"

        if self.tags:
            body = body + "Type: "
            for type_name in self.tags:
                body = body + " " + type_name.name
            body = body + "\n"
        return body

    @api.model
    def _send_email(self, sender, recipient, subject, body):
        tools.email_send(email_from=sender, email_to=[recipient],
                         subject=subject, body=body)

    @api.model
    def _log(self, message):
        print(message)

    @api.model
    def create(self, vals):
        postit = super(PrismePostit, self).create(vals)
        list_assigned_to = [item for item in postit.assigned_to if item]
        list_copy_to = [item for item in postit.copy_to if item]
        list_partners = set(list_assigned_to + list_copy_to)

        # names_users
        list_assigned_to_name = [item.name for item in postit.assigned_to if
                                 item]
        list_copy_to_name = [item.name for item in postit.copy_to if item]
        list_partners_names = (list_assigned_to_name + list_copy_to_name)

        postit.names_users = ', '.join(list_partners_names)
        # final names_users

        postit.message_ids[-1].body = postit.description
        ids = [i.partner_id.id for i in list_partners]
        postit.message_subscribe(ids, [])

        message = self.env['mail.message'].create({
            'subject': _('Invitation to follow %s: %s') % (
                postit._name, postit._name),
            'body': postit.description,
            'record_name': postit._name,
            'email_from': postit.env['mail.message']._get_default_from(),
            'reply_to': postit.env['mail.message']._get_default_from(),
            'model': postit._name,
            'res_id': postit.id,
            'no_auto_thread': True,
        })
        for item in ids:
            post_vars = {'subject': 'Notification',
                         'body': '#Postit - ' + postit.name + ' / ' +
                                 postit.description,
                         'partner_ids': [(4, item)],
                         }

            self.env['mail.thread'].message_post(
                type="notification", subtype="mt_comment", **post_vars)

        message.unlink()

        return postit

    @api.multi
    def _compute_opportunity_count(self):
        for postit in self:
            postit.opportunity_count = self.env['crm.lead'].search_count(
                [('postit_id', '=', postit.id)])

    @api.multi
    def redirect_crm_lead(self):
        action = self.env['ir.actions.act_window'].for_xml_id(
            'crm', 'crm_lead_opportunities')

        action['domain'] = [('postit_id', '=', self.id)]

        return action
