from odoo import models, fields 
from datetime import datetime, date

AVAILABLE_STATES  = [
    ('open','Open'),
    ('close','Close')
]

class SmartPosSession(models.Model):
    _name = 'smart.pos.session'


    def trans_close(self):
        #Calculate Total Payment Per Payment Method

        pass 

    
    name = fields.Char('Name', size=100)
    session_date = fields.Date('Session Date', default=date.today())
    date_open = fields.Datetime('Open Date Time', default=datetime.now())
    date_close = fields.Datetime('Close Date Time', default=datetime.now())
    smart_pos_config_id = fields.Many2one('smart.pos.config', 'Config', required=True)
    cashier_id = fields.Many2one('res.users', 'Cashier', required=True)
    smart_pos_order_ids = fields.One2many('smart.pos.order','smart_pos_session_id', 'Pos Orders')
    smart_pos_session_payment_ids = fields.One2many('smart.pos.session.payment', 'smart_pos_session_id', 'Pos Order Payments')
    state = fields.Selection(AVAILABLE_STATES, 'Status', default='open')
    

class SmartPosSessionPayment(models.Model):
    _name = 'smart.pos.session.payment'

    smart_pos_session_id = fields.Many2one('smart.pos.session', 'Pos Session #')
    smart_pos_payment_method_id = fields.Many2one('smart.pos.payment.method', 'Payment Method')
    amount_total = fields.Float('Amount Total')


