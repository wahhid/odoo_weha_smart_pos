from odoo import models, fields 


class SmartPosPaymentMethod(models.Model):
    _name = 'smart.pos.payment.method'

    name = fields.Char('Name', size=100, required=True)
    



    # id = Column(Integer, primary_key=True, autoincrement=True)
    # name = Column(String(100))