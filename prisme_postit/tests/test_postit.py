# -*- coding: utf-8 -*-
import mock
from odoo.tests.common import TransactionCase


class TestPostIt(TransactionCase):

    def setUp(self):
        super(TestPostIt, self).setUp()

        values = {
            'name': 'Teste',
            'description': 'Teste',
            'assigned_to': [(6, 0, self.env.ref('base.user_demo').ids)],
        }

        self.post_it = self.env['prisme.postit'].create(values)

    def test_action_in_process(self):
        self.assertNotEqual(self.post_it.state, 'in_process')
        self.assertFalse(self.post_it.date_start)

        # Realizamos o mock do Datetime.now para que o mesmo retorne
        # a data que desejamos. Isso e feito a fim de facilitar o teste.
        with mock.patch('odoo.fields.Datetime.now') as dt:
            dt.return_value = '2017-09-04 14:49:20'
            self.post_it.action_in_process()

        self.assertEqual(self.post_it.state, 'in_process')
        self.assertEqual(self.post_it.date_start, '2017-09-04')

    def test_action_close(self):
        self.assertNotEqual(self.post_it.state, 'terminated')
        self.assertFalse(self.post_it.date_end)

        # Realizamos o mock do Datetime.now para que o mesmo retorne
        # a data que desejamos. Isso e feito a fim de facilitar o teste.
        with mock.patch('odoo.fields.Datetime.now') as dt:
            dt.return_value = '2017-09-04 14:49:20'
            self.post_it.action_close()

        self.assertEqual(self.post_it.state, 'terminated')
        self.assertEqual(self.post_it.date_end, '2017-09-04')

    def test_action_active(self):
        self.post_it.state = 'terminated'
        self.assertNotEqual(self.post_it.state, 'active')
        self.post_it.action_active()
        self.assertEqual(self.post_it.state, 'active')
