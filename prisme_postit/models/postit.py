# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
from odoo import tools
from odoo import api, fields, models

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
    description = fields.Text()
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

    def init(self):
        self.env.cr.execute("""DROP TRIGGER IF EXISTS postit_update ON 
        prisme_postit_assignedto_rel;""")
        self.env.cr.execute("""CREATE OR REPLACE FUNCTION postit_update() 
        RETURNS trigger AS $$ BEGIN IF pg_trigger_depth() <> 1 THEN RETURN NEW;
        END IF; UPDATE prisme_postit SET names_users = subquery.string_agg
        FROM (SELECT ppar.prisme_postit_id,string_agg(partner.name, ', ') 
        FROM prisme_postit_assignedto_rel ppar JOIN res_users users ON 
        users.id=ppar.res_users_id JOIN res_partner partner ON 
        partner.id=users.partner_id GROUP BY ppar.prisme_postit_id) 
        AS subquery Where prisme_postit.id=subquery.prisme_postit_id; 
        RETURN NEW; END; $$ LANGUAGE plpgsql;""")
        self.env.cr.execute("""CREATE TRIGGER postit_update AFTER INSERT OR 
        UPDATE OR DELETE ON prisme_postit_assignedto_rel WHEN (
        pg_trigger_depth() < 1) EXECUTE PROCEDURE postit_update();""")

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
            if p.state != "closed":
                if p.recall_date:
                    recall_date = datetime.strptime(p.recall_date, "%Y-%m-%d")
                    if recall_date <= datetime.now():
                        if p.state == "start" or p.state == "in_process" or \
                                        p.state == "active":
                            if p.days:
                                weekday = p.days
                                for day in weekday:
                                    if datetime.now().weekday() == day.nbr:
                                        p._notify_recall(
                                            " en cours, echeance le ")

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

    def notificate_postit(self):
        message_id = self.message_ids[-1]
        mail_channel = self.env['mail.channel']

        list_assigned_to = [item for item in self.assigned_to if item]
        list_copy_to = [item for item in self.copy_to if item]

        list_partners = set([self.assigned_by] + list_assigned_to +
                            list_copy_to)
        list_partners = [item for item in list_partners if item]
        list_partners.sort()
        channel_id = mail_channel.search(
            [('channel_partner_ids', '=', [
                item.partner_id.id for item in list_partners]),
             ('name', '=', 'Postit %s' % ('/'.join(
                 [item.name for item in list_partners])))])
        channel_id = channel_id and channel_id[0]
        values = {}
        if not channel_id:
            values['name'] = 'Postit %s' % \
                             ('/'.join([item.name for item in list_partners]))
            values['public'] = 'public'

            values['channel_partner_ids'] = [
                (4, [item.partner_id.id for item in list_partners])]
            channel_id = mail_channel.create(values)

        message_id.channel_ids = [(6, 0, [channel_id.id])]
        message_id._notify()
