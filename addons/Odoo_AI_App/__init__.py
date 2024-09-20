# -*- coding: utf-8 -*-


from . import models
from odoo import api, SUPERUSER_ID

def uninstall_hook(cr, registry):
    cr.execute("""
                DELETE FROM ir_config_parameter WHERE key = 'openai_api_key'; """)

def install_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.config_parameter'].sudo().set_param('openai_api_key', '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')