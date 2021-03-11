from odoo import models, fields 


AVAILABLE_STATES = [
    ('unpaid','UnPaid'),
    ('paid', 'Paid'),
    ('hold', 'Hold'),
    ('cancel', 'Cancel')
]

class SmartPosOrder(models.Model):
    _name = 'smart.pos.order'

    name = fields.Char('Name', size=255)
    amount_paid = fields.Float('Amount Paid')
    amount_total = fields.Float('Amount Total')
    amount_tax = fields.Float('Amount Tax')
    amount_return = fields.Float('Amount Return')
    smart_pos_session_id = fields.Many2one('smart.pos.session', 'Session #')
    partner_id = fields.Many2one('res.partner', 'Customer')
    user_id = fields.Many2one('res.user', 'User #')
    state = fields.Selection()

    # id = Column(Integer, primary_key=True, autoincrement=True)
    # name = Column(String(255))
    # amount_paid = Column(Float)
    # amount_total = Column(Float)
    # amount_tax = Column(Float)
    # amount_return = Column(Float)
    # pos_session_id = Column(Integer, ForeignKey("pos_session.id"), nullable=True)
    # pos_session  = relationship("PosSession")
    # pricelist_id = Column(Integer)
    # partner_id = Column(Integer)
    # user_id = Column(Integer, ForeignKey("ab_user.id"), nullable=True)
    # user  = relationship("User")
    # employee_id = Column(Integer)
    # uid = Column(Integer)
    # sequence_number = Column(Integer)
    # creation_date = Column(DateTime)
    # fiscal_position_id = Column(Integer)
    # server_id = Column(Integer)
    # to_invoice = Column(Boolean)
    # state = Column(String(50), default='unpaid')


class SmartPosOrderLine(models.Model):
    _name = 'smart.pos.order.line'

class SmartPosOrderPayment(models.Model):
    _name = 'smart.pos.order.payment'