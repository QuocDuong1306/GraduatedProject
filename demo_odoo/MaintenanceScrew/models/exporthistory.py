from odoo import fields, models, api, _
from odoo.exceptions import UserError

class ExportHistory(models.Model):
    _name = 'export.history'
    _description = 'Export History'
    _rec_name = 'export_id'
    STATUS_SELECTION = [('new', 'New'), ('confirmed', 'Confirmed'), ('done', 'Done'),('cancel','Cancel')]

    export_id = fields.Char(string='Export ID',required=True, copy=False, readonly=True, default=lambda self: _('New'))
    warehouse_id = fields.Many2one('warehouse', string='Warehouse',store=True,required=True)
    factory_id = fields.Char(related='warehouse_id.factory_id.factory_id', string='ID Factory', store=True)
    name = fields.Char(related='warehouse_id.factory_id.name', string='Name of Factory', store=True)
    export_date = fields.Datetime(string='Export Completed Date',readonly=True)
    status = fields.Selection(selection=STATUS_SELECTION, string='Status', default='new',readonly=True)
    user_created = fields.Many2one('res.users', string='Created By',readonly=True, default=lambda self: self.env.user)
    user_confirmed = fields.Many2one('res.users', string='Confirmed By',readonly=True)#groups='MaintenanceScrew.group_employee_warehouse_staff')
    user_done = fields.Many2one('res.users', string='Done By',readonly=True)
    user_cancel = fields.Many2one('res.users',string='Cancel By', readonly=True)
    supplier = fields.Char(string='Supplier')
    description = fields.Text("Description")
    export_line_ids = fields.One2many('export.history.line', 'export_id', string='Export Lines')

    @api.model
    def create(self, values):
        if values.get('export_id', _('New')) == _('New'):
            values['export_id'] = self.env['ir.sequence'].next_by_code('export.history') or _('New')
        return super(ExportHistory, self).create(values)

    def write(self, vals):
        if self['export_id'] != 'New':
            if 'status' not in vals:
                raise UserError("You cannot edit a record.")
        return super(ExportHistory, self).write(vals)
    # @api.multi
    def action_confirm_export(self):
        for record in self:
            if record.status == 'new':
                record.write({'status': 'confirmed', 'user_confirmed': self.env.user.id})

    # @api.multi
    def action_done_export(self):
        for record in self:
            if record.status == 'confirmed':
                export_line_lst = record.env['export.history.line'].search([('export_id', '=', record.id)])
                for export_line in export_line_lst:
                    component_warehouse = export_line.env['component.warehouse'].search(
                        [('component_id', '=', export_line.component_id.id),
                         ('warehouse_id', '=', export_line.warehouse_id.id)])
                    if component_warehouse:
                        if component_warehouse.amount < export_line.export_amount:
                            raise UserError("The number of components is not enough to Export. Please Import and try again.")
                            return
                        else:
                            component_warehouse.amount -= export_line.export_amount
                    else:
                        export_line.env['component.warehouse'].create({
                            'component_id': export_line.component_id.id,
                            'warehouse_id': record.warehouse_id.id,
                            'amount': export_line.export_amount,
                            'reorder_min': 10,
                            'unit': 'piece',
                        })
                self.write({'status': 'done', 'user_done': self.env.user.id,
                            'export_date': fields.Datetime.now()})

    def action_cancel_export(self):
        view_id = self.env.ref('MaintenanceScrew.view_export_cancel').id
        return {
            'name': 'Cancel Task',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'export.cancel',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'views': [(view_id, 'form')],
            'context': {
                'default_task_id': self.id,
            },
        }


class ExportHistoryLine(models.Model):
    _name = 'export.history.line'
    _description = 'Export History Line'

    export_id = fields.Many2one('export.history', string='Export History ID')
    component_id = fields.Many2one('component', string='Component',required=True)
    status = fields.Selection(related='export_id.status', string='Status', store=True, readonly=True)
    export_date = fields.Datetime(related='export_id.export_date',string='Export Completed Date',readonly=True)
    component_serial = fields.Char(related='component_id.component_serial', string='Serial of Component', store=True,readonly=True)
    export_amount = fields.Integer(string='Export Amount',default=1)
    warehouse_id = fields.Many2one(related='export_id.warehouse_id', string='Warehouse', store=True, readonly=True)


