from odoo import models, fields 


class SmartPosProductCategory(models.Model):
    _name = 'smart.pos.product.category'

    name = fields.Char("Name", size=200, required=True)
    code = fields.Char("Code", size=4, required=True)
    