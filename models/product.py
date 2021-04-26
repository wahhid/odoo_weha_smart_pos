from odoo import models, fields 


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_avaiable_on_pos = fields.Boolean('Available on Pos', default=False)
    smart_pos_product_category_id = fields.Many2one('smart.pos.product.category', "Pos Product Category")
