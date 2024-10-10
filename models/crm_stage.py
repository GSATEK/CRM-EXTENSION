from odoo import models, fields

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    table_id = fields.Many2one('crm.table', string='CRM Table')
