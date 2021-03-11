from odoo import models, fields 


class SmartPosSession(models.Model):
    _name = 'smart.pos.session'

    name = fields.Char('Name', size=100)
