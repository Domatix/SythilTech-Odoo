# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
import requests
from openerp.http import request
import odoo

from openerp import api, fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    timesheet_default_project_id = fields.Many2one('project.project', string="Default Timesheet Project")

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.default'].set('res.config.settings', 'timesheet_default_project_id', self.timesheet_default_project_id.id)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            timesheet_default_project_id=self.env['ir.default'].get('res.config.settings', 'timesheet_default_project_id'),
        )
        return res
