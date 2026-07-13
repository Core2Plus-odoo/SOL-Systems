# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    arabic_name = fields.Char(string='Arabic Name')
    arabic_address = fields.Text(string='Arabic Address')
