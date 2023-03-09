from odoo import models, fields, _, api

class Warehouse(models.Model):
    _name = 'warehouse'
    _description = 'Warehouse'
    _rec_name = 'warehouse_id'

    warehouse_id = fields.Char(string='ID Warehouse', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    factory_id = fields.Many2one('factory', string='Factory', required=True)
    name = fields.Char(related='factory_id.name',string='Name of factory',store=True) # ten cua nha may
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')

    @api.model
    def create(self, values):
        if values.get('warehouse_id', _('New')) == _('New'):
            values['warehouse_id'] = self.env['ir.sequence'].next_by_code('warehouse') or _('New')
        return super(Warehouse, self).create(values)