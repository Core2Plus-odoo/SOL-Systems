# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    arabic_name = fields.Char(
        string='Arabic Name',
        help="Arabic product name shown under the English description on the "
             "bilingual tax invoice.")
