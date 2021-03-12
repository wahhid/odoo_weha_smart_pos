from odoo import models, fields 


class SmartPosPaymentMethod(models.Model):
    _name = 'smart.pos.payment.method'

    name = fields.Char('Name', size=100, required=True)