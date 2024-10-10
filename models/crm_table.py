from odoo import models, fields, api

class CrmTable(models.Model):
    _name = 'crm.table'
    _description = 'CRM Table'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    crm_stage_ids = fields.One2many('crm.stage', 'table_id', string='CRM Stages')
    active = fields.Boolean(string='Active', default=True)
    stage_count = fields.Integer(string='Stage Count', compute='_compute_stage_count')

    @api.depends('crm_stage_ids')
    def _compute_stage_count(self):
        for record in self:
            record.stage_count = len(record.crm_stage_ids)
