from odoo import models, fields, api, _

class Employee(models.Model):
    _name = 'employee'
    _description = 'Employee'
    _inherit = 'res.users'

    employee_id = fields.Char(string='ID Employee', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    image=fields.Binary(string='Picture of Employee',attachment=True)
    name = fields.Char(required=True)
    birthday = fields.Date(string='Birthday')
    position = fields.Selection([
        ('staff', 'Staff'),
        ('leader', 'Leader'),
        ('management', 'Management')
    ], required=True,string='Position')
    email = fields.Char(string='Email', required=True)
    # factory_id = fields.Many2one('factory', string='Factory')
    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email must be unique.')]
    @api.model
    def create(self, values):
        if values.get('employee_id', _('New')) == _('New'):
            values['employee_id'] = self.env['ir.sequence'].next_by_code('employee') or _('New')
        return super(Employee, self).create(values)
