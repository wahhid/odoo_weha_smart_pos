from odoo import models, fields 


class SmartPosConfig(models.Model):
    _name = 'smart.pos.config'

    name = fields.Char('Name', size=255, required=True)
    code = fields.Char('Code', size=5, required=True)
    currency_id = fields.Integer('Currency')
    pricelist_id = fields.Integer('Pricelist')
    company_id = fields.Many2one('res.company', 'Company', required=True)
    account_journal_id = fields.Many2one('account.journal', 'Journal')
    stock_picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type')
    smart_pos_payment_method_ids = fields.Many2many('smart.pos.payment.method', 'smart_pos_config_smart_pos_payment_method_rel', 'smart_pos_config_id', 'smart_pos_payment_method_id', 'Available Payment Methods') 
    
    # id = Column(Integer, primary_key=True, autoincrement=True)
    # name = Column(String(255), nullable=False)
    # code = Column(String(5), unique=True)
    # currency_id = Column(Integer)
    # pricelist_id = Column(Integer)
    # company_id = Column(Integer, ForeignKey("company.id"), nullable=True)
    # company = relationship("Company")
    # pos_payment_methods = relationship(
    #     "PosPaymentMethod", secondary=assoc_pos_config_pos_payment_method, backref="pos_config"
    # )
