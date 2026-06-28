# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    arabic_name = fields.Char(string='Arabic Name')
    arabic_address = fields.Text(string='Arabic Address')
