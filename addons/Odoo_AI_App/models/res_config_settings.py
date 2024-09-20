# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    openai_api_key = fields.Char(string="OpenAI API Key", config_parameter='openai_api_key', default='sk-vqjB06Fa5rZkHZanDy3vT3Blbk')
    openai_organization_id = fields.Char(string="OpenAI Organisation ID", config_parameter='openai_organization_id')
