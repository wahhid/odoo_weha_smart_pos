from odoo import models, fields 


class SmartPosPaymentMethod(models.Model):
    _name = 'smart.pos.payment.method'

    name = fields.Char('Name', size=100, required=True)
    code = fields.Char('Code', size=4, required=True)
    type = fields.Selection([('cash','Cash'),('bank','Bank'),('voucher','Voucher'),('point','Point')], 'Type', default='cash', required=True)