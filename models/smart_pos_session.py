from odoo import models, fields 
from datetime import datetime, date

AVAILABLE_STATES  = [
    ('open','Open'),
    ('close','Close')
]

class SmartPosSession(models.Model):
    _name = 'smart.pos.session'

    def trans_close(self):
        pass 

    
    name = fields.Char('Name', size=100)
    session_date = fields.Date('Session Date', default=date.today())
    date_open = fields.Datetime('Open Date Time', default=datetime.now())
    date_close = fields.Datetime('Close Date Time', default=datetime.now())
    smart_pos_config_id = fields.Many2one('smart.pos.config', 'Config', required=True)
    cashier_id = fields.Many2one('res.users', 'Cashier', required=True)
    state = fields.Selection(AVAILABLE_STATES, 'Status', default='open')
    

