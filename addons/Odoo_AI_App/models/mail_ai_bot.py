# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.tools import plaintext2html, html2plaintext


class MailBot(models.AbstractModel):
    _name = 'mail.ai.bot'
    _description = 'Mail AI Bot'

    def _answer_to_message(self, record, values):
        ai_bot_id = self.env['ir.model.data']._xmlid_to_res_id('openai_odoo_connector.partner_ai')
        if len(record) != 1 or values.get('author_id') == ai_bot_id or values.get('message_type') != 'comment':
            return
        if self._is_bot_in_private_channel(record):
            answer = self._get_answer(record)
            if answer:
                message_type = 'comment'
                subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment')
                record = record.with_context(mail_create_nosubscribe=True).sudo()
                record.message_post(body=answer, author_id=ai_bot_id, message_type=message_type, subtype_id=subtype_id)

    def _get_answer(self, record):
        partner_ai_id = self.env.ref('openai_odoo_connector.partner_ai')
        completion_id = self.env.ref('openai_odoo_connector.completion_chat')
        header = "This is a dialogue with an artificial intelligence helper."
        previous_message_ids = record.website_message_ids.filtered(lambda m: m.body != '')
        dialog = '\n'
        for message_id in previous_message_ids.sorted('create_date'):
            user_name = 'AI' if message_id.author_id == partner_ai_id else 'Human'
            dialog += f'{user_name}: {message_id.body}\n'

        res = completion_id.create_completion(prompt=header+dialog+'AI: ')
        return plaintext2html(html2plaintext(res[0]))

    def _is_bot_in_private_channel(self, record):
        ai_bot_id = self.env['ir.model.data']._xmlid_to_res_id('openai_odoo_connector.partner_ai')
        if record._name == 'mail.channel' and record.channel_type == 'chat':
            return ai_bot_id in record.with_context(active_test=False).channel_partner_ids.ids
        return False
