# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class OpenAicompletion(models.Model):
    _name = 'openai.completion'
    _description = 'OpenAI completion'
    _inherit = ['openai.mixin']

    def _get_openai_model_list(self):
        openai = self.get_openai()
        try:
            model_list = openai.Model.list()
        except Exception as e:
            raise ValidationError(e)

        res = [(m.id, m.id) for m in model_list.data]
        res.sort()
        return res

    def _get_post_process_list(self):
        return [('list_to_many2many', 'List to Many2many')]

    ai_model = fields.Selection(selection='_get_openai_model_list', string='AI Model', required=True)
    temperature = fields.Float(default=1)
    max_tokens = fields.Integer(default=16)
    top_p = fields.Float(default=1)
    frequency_penalty = fields.Float()
    presence_penalty = fields.Float()
    test_answer = fields.Text(readonly=True)
    post_process = fields.Selection(selection='_get_post_process_list')

    def create_completion(self, rec_id=0, prompt=''):
        openai = self.get_openai()
        if not prompt and rec_id:
            prompt = self.get_prompt(rec_id)
        try:
            res = openai.Completion.create(
                model=self.ai_model,
                prompt=prompt,
                max_tokens=self.max_tokens,
                n=self.n,
                temperature=self.temperature,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )
        except Exception as e:
            raise ValidationError(e)

        prompt_tokens = res.usage.prompt_tokens
        completion_tokens = res.usage.completion_tokens
        total_tokens = res.usage.total_tokens

        if rec_id:
            result_ids = []
            for choice in res.choices:
                answer = choice.text.strip()
                result_id = self.create_result(rec_id, prompt, answer, prompt_tokens, completion_tokens, total_tokens)
                result_ids.append(result_id)
            return result_ids
        else:
            return [choice.text.strip() for choice in res.choices]

    def openai_create(self, rec_id, method=False):
        return self.create_completion(rec_id)

    def create_result(self, rec_id, prompt, answer, prompt_tokens, completion_tokens, total_tokens):
        values = {'completion_id': self.id,
                  'model_id': self.model_id.id,
                  'target_field_id': self.target_field_id.id,
                  'res_id': rec_id,
                  'prompt': prompt,
                  'answer': answer,
                  'prompt_tokens': prompt_tokens,
                  'completion_tokens': completion_tokens,
                  'total_tokens': total_tokens,
                  }
        result_id = self.env['openai.completion.result'].create(values)
        return result_id

