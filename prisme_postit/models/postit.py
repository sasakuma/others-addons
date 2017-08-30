# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime

from odoo import tools
from odoo import api, fields, models
from odoo.tools.translate import _


class PrismePostIt(models.Model):
    _name = 'prisme.postit'
    _inherit = 'mail.thread'

    AVAILABLE_PRIORITIES = [
        ('0', 'Muito Baixa'),
        ('1', 'Baixa'),
        ('2', 'Normal'),
        ('3', 'Alta'),
        ('4', 'Muito Alta')]

    name = fields.Char(string='Name', required=True)

    names_users = fields.Char(string='Assigned to')

    description = fields.Text(required='True')

    assigned_by = fields.Many2one('res.users',
                                  string='Assigned by',
                                  default=lambda self: self._uid)

    assigned_to = fields.Many2many('res.users',
                                   'prisme_postit_assignedto_rel',
                                   string="Assigned to",
                                   required=True)

    copy_to = fields.Many2many('res.users',
                               'prisme_postit_copyto_rel',
                               string='Copy to')

    partner_id = fields.Many2one('res.partner', string='Client')

    priority = fields.Selection(string='Priority',
                                selection=AVAILABLE_PRIORITIES,
                                default='0',
                                index=True,
                                track_visibility='onchange')

    tags = fields.Many2many('prisme.postit.tag', string='Tags')
    days = fields.Many2many('prisme.postit.day', string='Days')

    date_start = fields.Date(string='Date start')

    recall_date = fields.Date(string='Date Recall')

    date_end = fields.Date(string='Date end')

    expected_date = fields.Date(string='Expected Date',
                                track_visibility='onchange')

    state = fields.Selection([('active', 'Non termine'),
                              ('in_process', 'En cours'),
                              ('terminated', 'Termine'),
                              ],
                             default='active',
                             track_visibility='onchange')

    active = fields.Boolean(default=True)

    @api.model
    def action_in_process(self):
        self.state = 'in_process'
        self.date_start = fields.Datetime.now()

    @api.model
    def action_close(self):
        self.state = 'terminated'
        self.date_end = fields.Datetime.now()

    @api.model
    def action_active(self):
        return self.write({'state': 'active'})

    @api.model
    def scheduled_action(self):

        domain = [
            ('state', 'in', ['start', 'in_process', 'active']),
            ('recall_date', '!=', False),
        ]

        postits = self.search(domain)

        for p in postits:
            recall_date = datetime.strptime(p.recall_date, '%Y-%m-%d')

            if recall_date <= datetime.now():
                weekday = p.days if p.days else []

                for day in weekday:
                    if datetime.now().weekday() == day.nbr:
                        p._notify_recall(' en cours, echeance le ')

    @api.model
    def _notify_recall(self, message):
        subject = self._construct_subject(message)
        body = self._construct_body()

        sender = ('Postit - OpenERP (%s) <system.openerp@prisme.ch>' %
                  self.env.cr.dbname)

        ass_by = self.assigned_by.email if self.assigned_by else False
        ignore_email = []

        if ass_by:
            # Sending e-mail to the user
            self._send_email(sender, ass_by, subject, body)
            ignore_email.append(ass_by)

        for ass_to in self.assigned_to:
            if ass_to.email not in ignore_email:
                self._send_email(sender, ass_to.email, subject, body)
                ignore_email.append(ass_to.email)

        for copy_to in self.copy_to:
            if copy_to not in ignore_email:
                self._send_email(sender, copy_to, subject, body)

    @api.model
    def _construct_subject(self, message):
        end_date_string = ''

        if self.date_end:
            end_date_string = '(%s)' % self.date_end

        return 'Postit (%s)%s%s' % (self.name, message, end_date_string)

    @api.model
    def _construct_body(self):

        body = "Rappel d'expiration de tache\n"
        body += '-------------------------------\n\n'

        body += 'Tache: %s\n' % self.name

        if self.assigned_by:
            body += 'Assign par: %s\n' % self.assigned_by.name

        if self.partner_id:
            body += 'Client: %s\n' % self.partner_id.name

        if self.date_start:
            body += 'Date de debut: %s\n' % self.date_start

        if self.date_end:
            body += 'Date limite: %s\n' % self.date_end

        if self.duration:
            body += 'Duree: %s\n' % self.duration

        if self.recall_date:
            body += 'Date echeance Postit: %s\n\n' % self.recall_date

        for ass_to in self.assigned_to:
            body += 'Assign a: %s\n' % ass_to.name

        for copy_to in self.copy_to:
            body += 'Copie a: %s\n\n' % copy_to.name

        if self.description:
            body += 'Description: \n%s\n\n' % self.description

        if self.tags:
            body += 'Type: '
            for type_name in self.tags:
                body += ' %s' % type_name.name
            body += '\n'
        return body

    @api.model
    def _send_email(self, sender, recipient, subject, body):
        tools.email_send(email_from=sender,
                         email_to=[recipient],
                         subject=subject,
                         body=body)

    @api.model
    def create(self, values):
        postit = super(PrismePostIt, self).create(values)

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
            'subject': _('Invitation to follow %s: %s') % (postit._name, postit._name),  # noqa: 501
            'body': postit.description,
            'record_name': postit._name,
            'email_from': postit.env['mail.message']._get_default_from(),
            'reply_to': postit.env['mail.message']._get_default_from(),
            'model': postit._name,
            'res_id': postit.id,
            'no_auto_thread': True,
        })

        for item in ids:
            post_vars = {
                'subject': u'Nova postit atribuído a você',
                'body': '#Postit - %s / %s' % (postit.name, postit.description),  # noqa: 501
                'partner_ids': [(4, item)],
                'message_type': 'notification',
                'subtype': 'mt_comment',
            }

            self.env['mail.thread'].message_post(**post_vars)

        message.unlink()

        return postit
