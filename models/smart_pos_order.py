from odoo import api, models, fields 
from odoo.exceptions import Warning, ValidationError

AVAILABLE_STATES = [
    ('unpaid','UnPaid'),
    ('paid', 'Paid'),
    ('hold', 'Hold'),
    ('cancel', 'Cancel')
]

class SmartPosOrder(models.Model):
    _name = 'smart.pos.order'

    def create_stock_picking(self):
        picking_type_id = smart_pos_session_id.smart_pos_config_id.stock_picking_type_id
        vals = {
            'partner_id': self.partner.id if self.partner else False,
            'user_id': False,
            'picking_type_id': 6,
            'location_id': stock_picking_type_id.default_location_src_id.id,
            'location_dest_id': location_dest_id.default_location_dest_id.id
        }

        stock_picking_id = self.env['stock.picking'].create(vals)
        if not stock_picking_id:
            raise Warning("Error picking process")

    name = fields.Char('Name', size=255)
    date_order = fields.Datetime('Order Date')
    amount_paid = fields.Float('Amount Paid')
    amount_total = fields.Float('Amount Total')
    amount_tax = fields.Float('Amount Tax')
    amount_return = fields.Float('Amount Return')
    smart_pos_session_id = fields.Many2one('smart.pos.session', 'Session #')
    partner_id = fields.Many2one('res.partner', 'Customer')
    user_id = fields.Many2one('res.users', 'User #')
    stock_picking_id = fields.Many2one('stock.picking','Picking #', readonly=True)
    smart_pos_order_line_ids = fields.One2many('smart.pos.order.line', 'smart_pos_order_id', 'Order Lines')
    smart_pos_order_payment_ids = fields.One2many('smart.pos.order.payment', 'smart_pos_order_id', 'Order Payments')
    state = fields.Selection(AVAILABLE_STATES, 'Status', default='unpaid')

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

    @api.model
    def create(self, vals):
        res = super(SmartPosOrder, self).create(vals)
        res.create_stock_picking()
        return res
        

class SmartPosOrderLine(models.Model):
    _name = 'smart.pos.order.line'

    smart_pos_order_id = fields.Many2one('smart.pos.order', 'Pos Order #')
    description = fields.Char('Description', size=250)
    product_id = fields.Many2one('product.template', 'Product')
    qty = fields.Float('Quantity', default=1.0)
    price_unit = fields.Float('Price')
    tax_id = fields.Many2one('account.tax', 'Tax')
    amount_tax = fields.Float('Amount Tax', default=0.0)
    amount_discount = fields.Float('Amount Discount', default=0.0)
    amount_total = fields.Float('Amount Total', default=0.0)
    

class SmartPosOrderPayment(models.Model):
    _name = 'smart.pos.order.payment'

    smart_pos_order_id = fields.Many2one('smart.pos.order', 'Pos Order #')
    smart_pos_payment_method_id = fields.Many2one('smart.pos.payment.method', 'Payment Method')
    discount_in_percentage = fields.Float('Discount %', default=0.0)
    amount_discount = fields.Float('Amount Discount', default=0.0)
    amount_total = fields.Float('Amount Total', default=0.0)
