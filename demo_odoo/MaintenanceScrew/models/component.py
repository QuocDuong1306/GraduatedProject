from odoo import fields, models, api, _


class Component(models.Model):
    _name = 'component'
    _description = 'Component'
    _rec_name = 'component_serial'

    component_id = fields.Char(string='Component ID', required=True, copy=False, readonly=True,
                               default=lambda self: _('New'))
    model_id = fields.Many2many('model', string='Model ID', required=True)
    component_serial = fields.Char(required=True, string='Serial')
    unit = fields.Selection([('piece', 'Piece'), ('lot', 'Lot')], string='Unit', required=True, default='piece')
    manufacturer = fields.Char(string='Manufacturer')
    description = fields.Text("Description")

    @api.model
    def create(self, values):
        if values.get('component_id', _('New')) == _('New'):
            values['component_id'] = self.env['ir.sequence'].next_by_code('component') or _('New')
        return super(Component, self).create(values)


class ComponentWarehouse(models.Model):
    _name = 'component.warehouse'
    _description = 'Component Warehouse'
    _rec_name = 'warehouse_id'

    component_id = fields.Many2one('component', string='Component')
    component_serial = fields.Char(related='component_id.component_serial', readonly=True, string='Serial of Component')
    warehouse_id = fields.Many2one('warehouse', string='Warehouse')
    amount = fields.Integer(string='Amount', readonly=True)
    unit = fields.Selection(related='component_id.unit', readonly=True, string='Unit')
    reorder_min = fields.Integer(string='Minimum Reorder Quantity',default=10)
    note = fields.Text("Note about component")


class ComponentReplaced(models.Model):
    _name = 'component.replaced'
    _description = 'Replaced Components for Maintenance'

    maintenance_id = fields.Many2one('maintenance', string='Maintenance', required=True)
    component_id = fields.Many2one('component', string='Component', required=True,
                                   domain="[('model_id','like',model_id)]")
    component_serial = fields.Char(related='component_id.component_serial', readonly=True, string='Serial of Component',
                                   )
    status = fields.Selection(related='maintenance_id.status', string='Status', store=True, readonly=True)
    reason = fields.Char(string='Reason for Replacement',required=True)
    quantity = fields.Integer(string='Quantity', required=True,default=1)
    model_id = fields.Char(related='maintenance_id.model_id',string= 'Model',readonly=True)

    @api.onchange('model_id')
    def check_machine_id(self):
        if self['component_id']:
            self['component_id'] = None


