from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    table_id = fields.Many2one('crm.table', string='CRM Table')
    stage_id = fields.Many2one(
        'crm.stage', string='Stage', index=True, tracking=True,
        compute='_compute_stage_id', readonly=False, store=True,
        copy=False, group_expand='_read_group_stage_ids', ondelete='restrict',
        domain="[('table_ids', '=', table_id), '|', ('team_id', '=', False), ('team_id', '=', team_id)]")


    @api.depends('table_id')
    def _compute_stage_id(self):
        for lead in self:
            if lead.table_id:
                if lead.table_id not in lead.stage_id.table_ids:
                    lead.stage_id = lead.stage_find(lead.table_id.id)
            else:
                lead.stage_id = False

    def stage_find(self, id):
        return self.env['crm.stage'].search([('table_ids.id', '=', id)], limit=1).id