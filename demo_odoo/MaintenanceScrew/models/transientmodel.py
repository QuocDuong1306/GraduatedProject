from odoo import api, fields, models


class CancelTaskImport(models.TransientModel):
    _name = 'import.cancel'

    task_id = fields.Many2one('import.history', readonly=True)
    reason = fields.Text(required=True, string="Reason")


    def confirm_cancel_task(self):
        self.task_id.write({
            'status': 'cancel',
            'description': self.reason,
            'user_cancel': self.env.user.id
        })

class CancelTaskExport(models.TransientModel):
    _name = 'export.cancel'

    task_id = fields.Many2one('export.history', readonly=True)
    reason = fields.Text(required=True, string="Reason")


    def confirm_cancel_task(self):
        self.task_id.write({
            'status': 'cancel',
            'description': self.reason,
            'user_cancel': self.env.user.id
        })