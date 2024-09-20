# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.users'

    def _init_messaging(self):
        if self._is_internal():
            self._init_ai_bot()
        return super()._init_messaging()

    def _init_ai_bot(self):
        self.ensure_one()
        ai_bot_id = self.env['ir.model.data']._xmlid_to_res_id('openai_odoo_connector.partner_ai')
        channel_info = self.env['mail.channel'].channel_get([ai_bot_id, self.partner_id.id])
        channel = self.env['mail.channel'].browse(channel_info['id'])
        return channel
