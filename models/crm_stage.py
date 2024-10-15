from odoo import models, fields, api

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    table_ids = fields.Many2many('crm.table', 'crm_stage_crm_table_rel', 'table_id', 'stage_id', string="Tablas")

    @api.model
    def name_create(self, name):
        res = super().name_create(name)
        context = self._context
        if res and context.get('active_model', '') == 'crm.table' and context.get('active_id'):
            # We create a default stage `new` for projects created on the fly.
            self.browse(res[0]).table_ids += self.env['crm.table'].sudo().search([
                ('id', '=', context.get('active_id'))
            ])
        return res
