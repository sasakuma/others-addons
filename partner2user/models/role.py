import time
from odoo import api, models


class ResUsersRole(models.Model):
    _inherit = 'res.users.role'

    @api.multi
    def copy(self, default=None):
        self.ensure_one()

        date_now = time.strftime("%Y-%m-%d %H:%M:%S")
        copy_name = self.name + u' ' + date_now

        group_dict = self._generate_dict_from_record(self.group_id)
        group_dict['name'] = copy_name
        group_rec = self.env['res.groups'].create(group_dict)

        role_dict = self._generate_dict_from_record(self)
        role_dict['name'] = copy_name
        role_dict['group_id'] = group_rec.id
        role_dict['line_ids'] = False

        return self.env['res.users.role'].create(role_dict)

    def _generate_dict_from_record(self, rec, record_dict=None):
        """
        :param rec: Record that will be used to examine type of each field
                       to adjust it in case of relational type.
        :param record_dict: Base dict containing each field of 'rec' object.
        :return: record_dict with fields of relational type readjusted.
        """
        if rec:
            record_dict = rec.read()[0] if record_dict is None else record_dict

            date_fields_to_avoid = ['create_date', 'write_date', 'id',
                                    'create_uid', 'write_uid']

            for field in date_fields_to_avoid:
                if field in record_dict:
                    record_dict.pop(field)

            dic_fields_to_avoid = {
                **rec._field_inverses._map,
                **rec._field_computed,
            }

            for field in dic_fields_to_avoid:
                if (rec._fields[field.name].type != 'one2many' and
                            field.name in record_dict):
                    record_dict.pop(field.name)
                    continue

            readjusted_dict = dict(record_dict)

            for field in record_dict:
                if not rec[field]:
                    readjusted_dict.pop(field)
                elif rec._fields[field].type == 'many2one' and rec[field]:
                    readjusted_dict[field] = rec[field].id

                elif rec._fields[field].type == 'many2many' and rec[field]:
                    many2many_lines = []
                    for line in rec[field]:
                        many2many_lines.insert(0, line.id)
                    readjusted_dict[field] = [(6, 0, many2many_lines)]

            return readjusted_dict
