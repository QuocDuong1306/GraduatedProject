from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ModelCategory(models.Model):
    _name = 'model.category'
    _description = 'Model Category'
    _rec_name = 'category'

    category_id = fields.Char("Category ID",required=True, copy=False, readonly=True,
                              default=lambda self: _('New'))
    category = fields.Char("Category",require=True)

    @api.model
    def create(self, values):
        if values.get('category_id', _('New')) == _('New'):
            values['category_id'] = self.env['ir.sequence'].next_by_code('model.category') or _('New')
        return super(ModelCategory, self).create(values)

class ModelGroup(models.Model):
    _name = 'model.group'
    _description = 'Model Group'
    _rec_name = 'group'

    category = fields.Many2one('model.category',required=True,string='Category')
    group = fields.Char("Group",require=True)

    def button_detail(self):
        for rec in self:
            a = rec.group
            return {
                'type': 'ir.actions.act_window',
                'name': a,
                'res_model': 'model',
                'domain': [('group', '=', a)],
                'view_mode': 'kanban,tree,form',
                'target': 'current',
            }

class Model(models.Model):
    _name = 'model'
    _description = 'Model'
    _rec_name = 'model_name'

    model_id=fields.Char("Model ID",required=True, copy=False, readonly=True,
                              default=lambda self: _('New'))

    group= fields.Many2one('model.group',string='Group',required=True)
    category = fields.Many2one('model.category',string='Category',required=True)
    model_name=fields.Char("Model Name",require=True)
    manufacturer=fields.Char("Manufacturer")
    description=fields.Text("Description")
    model_list_ids = fields.One2many('model.list','model_name',string="Part List")
    photo1=fields.Binary("Model's Picture")
    image_ids = fields.One2many('model.list.photo', 'model_name', string='Part Scan')


    @api.model
    def create(self, values):
        if values.get('model_id', _('New')) == _('New'):
            values['model_id'] = self.env['ir.sequence'].next_by_code('model') or _('New')
        return super(Model, self).create(values)

class ModelList(models.Model):
    _name = 'model.list'
    _description = 'Model List'
    _rec_name = 'component_serial'

    model_name = fields.Many2one('model',string="Model",required=True)
    no = fields.Integer(string='No',required=True,default=1)
    component_serial = fields.Many2one('component',string='Component Serial',required=True)
    description = fields.Text (string='Description')

class ModelListPhoto(models.Model):
    _name = 'model.list.photo'
    _description = 'Model List Photo'
    _rec_name = 'no'


    model_name = fields.Many2one('model',string="Model",required=True)
    no = fields.Integer(string='No',required=True,default=1)
    image = fields.Binary(string='Image',required=True,attachment=True)
