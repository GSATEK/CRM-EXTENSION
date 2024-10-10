from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    table_id = fields.Many2one('crm.table', string='CRM Table', compute='_compute_table_id')

    @api.depends('stage_id')
    def _compute_table_id(self):
        for lead in self:
            lead.table_id = lead.stage_id.table_id
