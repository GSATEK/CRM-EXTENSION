from odoo import models, fields, api

class CrmTable(models.Model):
    _name = 'crm.table'
    _description = 'CRM Table'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    stage_count = fields.Integer(string='Stage Count', compute='_compute_stage_count')
    crm_stage_ids = fields.Many2many('crm.stage', 'crm_stage_crm_table_rel', 'stage_id', 'table_id', string="Etapas")


    @api.depends('crm_stage_ids')
    def _compute_stage_count(self):
        for record in self:
            record.stage_count = len(record.crm_stage_ids)

    def action_view_crm_lead_table(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Odoo - Oportunidades',
            'res_model': 'crm.lead',
            'view_mode': 'kanban',
            'domain': [('table_id', '=', self.id)],
        }