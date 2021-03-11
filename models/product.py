from odoo import models, fields 


class ProductTemplate(models.Model):
    _name = 'product.template'

    is_avaiable_on_pos = fields.Boolean('Available on Pos', default=False)