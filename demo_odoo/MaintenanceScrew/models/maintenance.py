from odoo import fields, models, api, _
from odoo.exceptions import UserError


class Maintenance(models.Model):
    _name = 'maintenance'
    _description = 'Maintenance'

    TYPE_SELECTION = [
        ('daily', 'Daily Check'),
        ('period', 'Period Check'),
    ]

    STATUS_SELECTION = [
        ('draft', 'Draft'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('cancel','Cancel'),
    ]

    maintenance_id = fields.Char(string='Maintenance ID', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    type = fields.Selection(TYPE_SELECTION, string='Type', required=True, default='preventive')
    datetime_start = fields.Datetime(string='Start Date', required=True, default=fields.Datetime.now,readonly=True)
    datetime_finished = fields.Datetime(string='Finish Date', readonly=True)
    worktime = fields.Float(string='Work Time (hours)',readonly=True, compute='_compute_worktime') # định chuyển sang hours:min
    user_created = fields.Many2one('res.users', string='User', required=True,readonly=True, default=lambda self: self.env.user)
    user_done = fields.Many2one('res.users', string='Done By', readonly=True)
    user_cancel = fields.Many2one('res.users',string='Cancel By', readonly=True)
    status = fields.Selection(STATUS_SELECTION, string='Status', required=True,readonly=True, default='draft')
    component_ids = fields.One2many('component.replaced', 'maintenance_id', string='Replaced Component')
    description = fields.Text(string='Description')
    photo = fields.Binary(string='Photo')

    factory_id = fields.Many2one('factory', string='Factory', required=True)
    machine_id = fields.Many2one('machine',string='Machine', required=True,domain="[('factory_id','=',factory_id)]")
    model_id = fields.Char(related='machine_id.model_id.model_name')
    floor = fields.Integer(string="Floor",readonly=True)
    location_x = fields.Integer(string="Floor",readonly=True)
    location_y = fields.Integer(string="Floor",readonly=True)
    @api.onchange('factory_id')
    def check_machine_id(self):
        for rec in self:
            if rec['machine_id']:
                rec['machine_id'] = None
                rec['floor'] = None
                rec['location_x'] = None
                rec['location_y'] = None

    @api.onchange('machine_id')
    def check_location(self):
        for rec in self:
            machine_location_id = rec.env['machine.location'].search([('machine_id','=',rec.machine_id.id)])
            if machine_location_id:
                # machine_location = rec.env['machine.location'].browse(machine_location_id)
                rec['floor'] = machine_location_id['floor']
                rec['location_x'] = machine_location_id['location_x']
                rec['location_y'] = machine_location_id['location_y']
            rec['component_ids'] = None

    @api.model
    def create(self, values):
        if values.get('maintenance_id', _('New')) == _('New'):
            values['maintenance_id'] = self.env['ir.sequence'].next_by_code('maintenance') or _('New')

        values['status'] = 'processing'
        return super(Maintenance, self).create(values)

    def write(self, vals):
        if self['maintenance_id'] != 'New':
            if 'status' not in vals:
                raise UserError("You cannot edit a record.")
        return super(Maintenance, self).write(vals)

    def action_done(self):
            self.write({'status': 'done', 'user_done': self.env.user.id,
                        'datetime_finished': fields.Datetime.now()})



    def action_cancel(self):
            if self.status == 'processing' or self.status=='draft':
                self.write({'status': 'cancel', 'user_cancel': self.env.user.id})

    @api.depends('datetime_start', 'datetime_finished')
    def _compute_worktime(self):
        for record in self:
            if record.datetime_finished:
                delta = fields.Datetime.from_string(record.datetime_finished) - fields.Datetime.from_string(record.datetime_start)
                record.worktime = delta.total_seconds() / 3600.0
            else:
                record.worktime = 0.0



