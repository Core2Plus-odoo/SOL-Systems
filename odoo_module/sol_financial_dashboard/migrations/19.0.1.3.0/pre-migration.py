# -*- coding: utf-8 -*-
"""Ensure the product_template.arabic_name column exists before the models load.

A stored field only gets its DB column when the module's schema upgrade runs.
Adding this field once caused an UndefinedColumn crash because the deploy
loaded the new code without creating the column. Creating it here (guarded by
IF NOT EXISTS) makes the upgrade self-healing regardless of ordering.
"""


def migrate(cr, version):
    cr.execute(
        "ALTER TABLE product_template "
        "ADD COLUMN IF NOT EXISTS arabic_name varchar"
    )
