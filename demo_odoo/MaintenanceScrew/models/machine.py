from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class Machine(models.Model):
    _name = 'machine'
    _description = 'Machine'
    _rec_name = 'machine_serial'

    machine_id = fields.Char(string='Machine ID', required=True, copy=False, readonly=True,
                              default=lambda self: _('New'))
    model_id = fields.Many2one('model',string='Model', required=True)
    factory_id = fields.Many2one('factory', string='Factory', required=True)
    name = fields.Char(related='factory_id.name', string='Name of factory', store=True,readonly=True)
    machine_serial = fields.Char(string='Machine Serial',required=True)
    date_added = fields.Date(string='Date Added',required=True)
    qr_code = fields.Binary(string='QR Code')
    # manufacturer = fields.Char(string='Manufacturer')
    machine_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], required=True, default='active', string='Machine Status')
    scheduled_maintenance = fields.Date(string='Scheduled maintenance date',readonly=True)
    note = fields.Text("Write your note about this Machine")
    photo=fields.Binary("Machine's Picture",attachment=True)
    @api.model
    def create(self, values):
        if values.get('machine_id', _('New')) == _('New'):
            values['machine_id'] = self.env['ir.sequence'].next_by_code('machine') or _('New')
        return super(Machine, self).create(values)

class MachineLocation(models.Model):
        _name = 'machine.location'
        _description = 'Machine Location'

        machine_id = fields.Many2one('machine', string='Machine', required=True)
        machine_serial = fields.Char(related='machine_id.machine_serial', string='Machine serial', store=True,readonly=True)
        factory_id = fields.Char(related='machine_id.factory_id.factory_id', string='ID Factory', store=True,readonly=True)
        name = fields.Char(related='machine_id.factory_id.name', string='Name of Factory', store=True,readonly=True)
        floor = fields.Integer(string='Floor', required=True,group_operator=False)
        location_x = fields.Integer(string='Location X', required=True,group_operator=False)
        location_y = fields.Integer(string='Location Y', required=True,group_operator=False)


        _sql_constraints = [
         ('unique_machine_location', 'unique(machine_id)', 'A machine location already exists for this machine.')]



        # kiểm tra điều kiện khi sửa, nếu như nhập 1 thì kiểm tra 1 , nhập 2 thì kiểm tra 2, nhập 3 thì kiểm tra 3
        # def write(self, vals):
        #     a = self.env['machine.location'].search(
        #         [('floor', '=', vals['floor']), ('location_x', '=', vals['location_x']),
        #          ('location_y', '=', vals['location_y'])])
        #     if a:
        #         raise UserError('This location is match with another machine.')
        #     return super(MachineLocation, self).write(vals)

        @api.onchange('floor','location_x','location_y')
        def check_location(self):
            for rec in self:
               if rec.floor:
                   a = rec.env['machine.location'].search(
                           [('floor', '=', rec.floor), ('location_x', '=', rec.location_x),
                            ('location_y', '=', rec.location_y)])
                   if a:
                       raise UserError('This location is match with another machine.')

               if rec.location_x:
                   a = rec.env['machine.location'].search(
                       [('floor', '=', rec.floor), ('location_x', '=', rec.location_x),
                        ('location_y', '=', rec.location_y)])
                   if a:
                       raise UserError('This location is match with another machine.')


               if rec.location_y:
                   a = rec.env['machine.location'].search(
                       [('floor', '=', rec.floor), ('location_x', '=', rec.location_x),
                        ('location_y', '=', rec.location_y)])
                   if a:
                       raise UserError('This location is match with another machine.')


class Model(models.Model):
    _name = 'model'
    _description = 'Model'
    _rec_name = 'model_name'

    model_id=fields.Char("Model ID",required=True, copy=False, readonly=True,
                              default=lambda self: _('New'))
    model_name=fields.Char("Model Name",require=True)
    manufacturer=fields.Char("Manufacturer")
    description=fields.Text("Description")

    @api.model
    def create(self, values):
        if values.get('model_id', _('New')) == _('New'):
            values['model_id'] = self.env['ir.sequence'].next_by_code('model') or _('New')
        return super(Model, self).create(values)

