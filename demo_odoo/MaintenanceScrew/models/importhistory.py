from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ImportHistory(models.Model):
    _name = 'import.history'
    _description = 'Import History'
    _rec_name = 'import_id'
    STATUS_SELECTION = [('new', 'New'), ('confirmed', 'Confirmed'), ('done', 'Done'),('cancel','Cancel')]

    import_id = fields.Char(string='Import ID',required=True, copy=False, readonly=True, default=lambda self: _('New'))
    warehouse_id = fields.Many2one('warehouse', string='Warehouse',store=True,required=True)
    factory_id = fields.Char(related='warehouse_id.factory_id.factory_id', string='ID Factory', store=True)
    name = fields.Char(related='warehouse_id.factory_id.name', string='Name of Factory', store=True)
    import_date = fields.Datetime(string='Import Completed Date',readonly=True)
    status = fields.Selection(selection=STATUS_SELECTION, string='Status', default='new',readonly=True)
    user_created = fields.Many2one('res.users', string='Created By',readonly=True, default=lambda self: self.env.user)
    user_confirmed = fields.Many2one('res.users', string='Confirmed By',readonly=True)#groups='MaintenanceScrew.group_employee_warehouse_staff')
    user_done = fields.Many2one('res.users', string='Done By',readonly=True)
    user_cancel = fields.Many2one('res.users',string='Cancel By', readonly=True)
    supplier = fields.Char(string='Supplier')
    description = fields.Text("Description")
    import_line_ids = fields.One2many('import.history.line', 'import_id', string='Import Lines')

    @api.model
    def create(self, values):
        if values.get('import_id', _('New')) == _('New'):
            values['import_id'] = self.env['ir.sequence'].next_by_code('import.history') or _('New')
        return super(ImportHistory, self).create(values)

    def write(self, vals):
        if self['import_id'] != 'New':
            if 'status' not in vals:
                raise UserError("You cannot edit a record.")
        return super(ImportHistory, self).write(vals)
    # @api.multi
    def action_confirm(self):
        for record in self:
            if record.status == 'new':
                record.write({'status': 'confirmed', 'user_confirmed': self.env.user.id})

    # @api.multi
    def action_done(self):
        for record in self:
            if record.status == 'confirmed':
                import_line_lst = record.env['import.history.line'].search([('import_id', '=', record.id)])
                for import_line in import_line_lst:
                    component_warehouse = import_line.env['component.warehouse'].search(
                        [('component_id', '=', import_line.component_id.id),
                         ('warehouse_id', '=', import_line.warehouse_id.id)])
                    if component_warehouse:
                        component_warehouse.amount += import_line.import_amount
                    else:
                        import_line.env['component.warehouse'].create({
                            'component_id': import_line.component_id.id,
                            'warehouse_id': record.warehouse_id.id,
                            'amount': import_line.import_amount,
                            'reorder_min': 10,
                            'unit': 'piece',
                        })
                self.write({'status': 'done', 'user_done': self.env.user.id,
                            'import_date': fields.Datetime.now()})


    def action_cancel(self):
        view_id = self.env.ref('MaintenanceScrew.view_import_cancel').id
        return {
            'name': 'Cancel Task',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.cancel',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'views': [(view_id, 'form')],
            'context': {
                'default_task_id': self.id,
            },
        }



class ImportHistoryLine(models.Model):
    _name = 'import.history.line'
    _description = 'Import History Line'

    import_id = fields.Many2one('import.history', string='Import History ID')
    component_id = fields.Many2one('component', string='Component',required=True)
    status = fields.Selection(related='import_id.status', string='Status', store=True, readonly=True)
    import_date = fields.Datetime(related='import_id.import_date',string='Import Completed Date',readonly=True)
    component_serial = fields.Char(related='component_id.component_serial', string='Serial of Component', store=True,readonly=True)
    import_amount = fields.Integer(string='Import Amount',default=1)
    # warehouse_id = fields.Char(related='import_id.warehouse_id.warehouse_id',store=True,readonly=True,string='Warehouse')
    warehouse_id = fields.Many2one(related='import_id.warehouse_id', string='Warehouse', store=True, readonly=True)


