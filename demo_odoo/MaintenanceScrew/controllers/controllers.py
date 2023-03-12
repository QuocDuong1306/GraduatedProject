from odoo import http
from odoo.http import request


class MachineAPI(http.Controller):

    @http.route('/api/machine/<int:id>', type='json', auth='user')
    def get_machine_info(self, id, **kwargs):
        machine = request.env['machine'].sudo().search([('id', '=', id)])
        if not machine:
            return http.Response(status=404)
        machine_data = {
            'id': machine.id,
            'machine_id': machine.machine_id,
            # 'model_id': machine.model_id.name,
            'factory_name': machine.factory_id.name,
            'machine_serial': machine.machine_serial,
            'date_added': machine.date_added,
            'machine_status': machine.machine_status,
            'scheduled_maintenance': machine.scheduled_maintenance,
            'note': machine.note,
            # 'photo': machine.photo,
        }
        return machine_data


    @http.route('/machine_models', auth='user', type='json')
    def get_machine_models_info(self, **kwargs):
        machine_models = request.env['machine'].sudo().search([])
        machine_models_data = []
        for machine_model in machine_models:
            machine_model_data = {
                'id': machine_model.id,
                'machine_id': machine_model.machine_id,
                'name': machine_model.machine_serial,
                'description': machine_model.note,
            }
            machine_models_data.append(machine_model_data)
        return machine_models_data
