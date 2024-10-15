from odoo import models, fields

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    table_ids = fields.Many2many('crm.table', 'crm_stage_crm_table_rel', 'table_id', 'stage_id', string="Tablas")
