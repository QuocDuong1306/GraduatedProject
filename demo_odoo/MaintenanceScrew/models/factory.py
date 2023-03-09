from odoo import models, fields, _, api

class Factory(models.Model):
    _name = 'factory'
    _description = 'Factory'
    _rec_name = 'name'

    factory_id = fields.Char(string='ID Factory', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    name = fields.Char(required=True, string='Name of Factory')
    location = fields.Char(string='Location',required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    machine_ids = fields.One2many('machine', 'factory_id', string='Machine List')

    @api.model
    def create(self, values):
        if values.get('factory_id', _('New')) == _('New'):
            values['factory_id'] = self.env['ir.sequence'].next_by_code('factory') or _('New')
        return super(Factory, self).create(values)