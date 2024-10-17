from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    table_id = fields.Many2one('crm.table', string='CRM Table')
    stage_id = fields.Many2one(
        'crm.stage', string='Stage', index=True, tracking=True,
        compute='_compute_stage_id', readonly=False, store=True,
        copy=False, group_expand='_read_group_stage_ids', ondelete='restrict',
        domain="[('table_ids', '=', table_id), '|', ('team_id', '=', False), ('team_id', '=', team_id)]")

    @api.model_create_multi
    def create(self, vals_list):
        new_vals_list = []
        context = self._context
        for vals in vals_list:
            new_vals = vals.copy()
            if 'table_id' is not vals and context.get('active_model', '') == 'crm.table' and context.get('active_id'):
                new_vals['table_id'] = context.get('active_id')
            new_vals_list.append(new_vals)

        return super(CrmLead, self).create(new_vals_list)


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

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        if domain:
            for item in domain:
                if len(item) == 3:
                    if item[0] == 'table_id':
                        search_domain.append(('table_ids.id', item[1], item[2]))

        stage_ids = stages.sudo()._search(search_domain, order=order)
        result = stages.browse(stage_ids)
        return result