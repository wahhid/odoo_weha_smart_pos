import re
import ast
import functools
from datetime import datetime, date
import logging
import json
import werkzeug.wrappers
from odoo.exceptions import AccessError
from odoo.addons.weha_smart_pos.common import invalid_response, valid_response
import sys
import pytz
from odoo import http

from odoo.addons.weha_smart_pos.common import (
    extract_arguments,
    invalid_response,
    valid_response,
)


from odoo.http import request


_logger = logging.getLogger(__name__)

def validate_token(func):
    """."""

    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        """."""
        access_token = request.httprequest.headers.get("access_token")
        if not access_token:
            return invalid_response("access_token_not_found", "missing access token in request header", 401)
        access_token_data = (
            request.env["api.access_token"].sudo().search([("token", "=", access_token)], order="id DESC", limit=1)
        )

        if access_token_data.find_one_or_create_token(user_id=access_token_data.user_id.id) != access_token:
            return invalid_response("access_token", "token seems to have expired or invalid", 401)

        request.session.uid = access_token_data.user_id.id
        request.uid = access_token_data.user_id.id
        return func(self, *args, **kwargs)

    return wrap


class WehaSmartPosController(http.Controller):
    @http.route(['/smart_pos/pos',], type='http', auth="user", csrf=False)
    def pos(self, **args):
        return http.request.render('weha_smart_pos.pos_screen',{})

    @validate_token
    @http.route("/api/smartpos/v1.0/uploadtransaction", type="json", auth="none", methods=["POST"], csrf=False)
    def pos_upload_transaction(self, **post):
        try:
            data = json.loads(request.httprequest.data)
            _logger.info(data)  
            #Check POS Session
            domain = [
                ('name','=', data['smart_pos_session_id']['name'])
            ]
            pos_session_id = http.request.env['smart.pos.session'].search(domain, limit=1)
            if not pos_session_id:
                #Find POS Config
                domain = [
                    ('code','=', data['smart_pos_session_id']['config_id']['code'])
                ]
                pos_config_id = http.request.env['smart.pos.config'].search(domain, limit=1)
                if not pos_config_id:
                    data =  {
                        "err": True,
                        "message": "POS Config not found",
                        "data": []
                    }
                    data
                            
                #Create POS Session
                pos_session = {
                    "name":  data['smart_pos_session_id']['name'],
                    "smart_pos_config_id": pos_config_id.id,
                    "cashier_id": data['user_id'],
                    "session_date":  data['smart_pos_session_id']['session_date'],
                    "date_open":  data['smart_pos_session_id']['date_open'],
                }
                pos_session_id = http.request.env['smart.pos.session'].create(pos_session)
                if not pos_session_id:
                    data =  {
                        "err": True,
                        "message": "Error Create POS Session",
                        "data": []
                    }
                    return data

            pos_order = {
                "name": data['name'],
                "user_id": data['user_id'],
                "date_order": data['date_order'],
                "smart_pos_session_id": pos_session_id.id,
                "amount_total": data['amount_total'],
                "amount_paid": data['amount_paid'],
                "state": data['state'],
            }

            pos_order_id = http.request.env['smart.pos.order'].create(pos_order)

            smart_pos_order_line_ids = []
            for smart_pos_order_line_id in data['smart_pos_order_line_ids']:
                pos_order_line = (0,0, {
                    "description": smart_pos_order_line_id["description"],
                    "product_id": smart_pos_order_line_id["product_id"],
                    "qty": smart_pos_order_line_id["qty"],
                    "price_unit": smart_pos_order_line_id["price_unit"],
                    "tax_id": False,
                    "amount_tax": 0,
                    "amount_discount": 0,
                    "amount_total": smart_pos_order_line_id["amount_total"]
                }) 
                smart_pos_order_line_ids.append(pos_order_line)
            pos_order_id.write({'smart_pos_order_line_ids': smart_pos_order_line_ids})

            smart_pos_order_payment_ids = []
            for smart_pos_order_payment_id in data['smart_pos_order_payment_ids']:
                pos_order_payment = (0,0, {
                    "smart_pos_payment_method_id": 1,
                    "discount_in_percentage": 0.0,
                    "amount_discount": 0.0,
                    "amount_total": 12000
                })
                smart_pos_order_payment_ids.append(pos_order_payment)
            pos_order_id.write({'smart_pos_order_payment_ids': smart_pos_order_payment_ids})
            data =  {
                "err": False,
                "message": "Success",
                "data": [{
                    "pos_order_id": pos_order_id.id
                }]
            }
            #return valid_response(data)
            return data
        except Exception as e:
            data =  {
                "err": True,
                "message": e,
                "data": []
            }
            return data

    @validate_token
    @http.route("/api/smartpos/v1.0/createpossession", type="http", auth="none", methods=["POST"], csrf=False)
    def pos_create_pos_session(self, **post):
        name = post['name'] or False if 'name' in post else False
        smart_pos_config_id = post['smart_pos_config_id'] or False if 'smart_pos_config_id' in post else False
        cashier_id = post['cashier_id'] or False if 'cashier_id' in post else False

        _fields_includes_in_body = all([name, 
                                        smart_pos_config_id, 
                                        cashier_id])
                                        
        if not _fields_includes_in_body:
                data =  {
                    "err": True,
                    "message": "Missing fields",
                    "data": []
                }
                return valid_response(data)

        #Check Smart Pos Config
        smart_pos_config_id = http.request.env['smart.pos.config'].search([('code','=', )])
        domain = [
            ('smart_pos_config_id', '=', data['smart_pos_config_id']),
            ('cashier_id', '=', data['cashier_id'])
        ]

        _logger.info(domain)
        vals = []
        output = []
        return json.dumps({"err": False, "message": "Success", "data":[]})

    @validate_token
    @http.route("/api/smartpos/v1.0/createposorder", type="json", auth="none", methods=["POST"], csrf=False)
    def pos_create_pos_order(self, **post):
        data = json.loads(request.httprequest.data)
        #Data Example
        # {
        #     "smart_pos_config_id": 1,
        #     "cashier_id": 1,
        #     "smart_pos_session_id": 1,
        #     "amount_total": 12000,
        #     "amount_paid": 12000,
        #     "smart_pos_order_line_ids": [
        #         {
        #             "description": "Fanta",
        #             "product_id": 1,
        #             "qty": 1,
        #             "price_unit": 12000,
        #             "tax_id": false,
        #             "amount_tax": 0,
        #             "amount_discount": 0,
        #             "amount_total": 12000
        #         }
        #     ],
        #     "smart_pos_order_payment_ids": [
        #         {
        #             "smart_pos_payment_method_id": 1,
        #             "discount_in_percentage": 0.0,
        #             "amount_discount": 0.0,
        #             "amount_total": 12000
        #         }
        #     ]
        # }
        # Create Pos Order
        vals = {
            "name": data['name'],
            "date_order": datetime.strptime(data['date_order'],'%Y-%m-%d %H:%M:%S').astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S'),
            "user_id": data['user_id'],
            "smart_pos_session_id": data['smart_pos_session_id'],
            "amount_total": data['amount_total'],
            "amount_paid": data['amount_paid'],
            "state": "paid"
        }
        #Create Pos Order Line
        order_line_ids = []
        for smart_pos_order_line_id in data['smart_pos_order_line_ids']:
            line_vals = (0,0,
                {
                    "description": smart_pos_order_line_id['description'],
                    "product_id": smart_pos_order_line_id['product_id'],
                    "qty": smart_pos_order_line_id['qty'],
                    "price_unit": smart_pos_order_line_id['price_unit'],
                    "tax_id": smart_pos_order_line_id['tax_id'],
                    "amount_tax": smart_pos_order_line_id['amount_tax'],
                    "amount_discount": smart_pos_order_line_id['amount_discount'],
                    "amount_total": smart_pos_order_line_id['amount_total'],
                }
            )
            order_line_ids.append(line_vals)
        vals.update({"smart_pos_order_line_ids": order_line_ids})

        #Create Pos Order Payment
        payment_line_ids = []
        for smart_pos_order_payment_id in data['smart_pos_order_payment_ids']:
            line_vals = (0,0, 
                {
                    "smart_pos_payment_method_id": smart_pos_order_payment_id['smart_pos_payment_method_id'],
                    "discount_in_percentage": smart_pos_order_payment_id['discount_in_percentage'],
                    "amount_discount": smart_pos_order_payment_id['amount_discount'],
                    "amount_total": smart_pos_order_payment_id['amount_total']   
                }
            )
            payment_line_ids.append(line_vals)
        vals.update({"smart_pos_order_payment_ids": payment_line_ids})
        
        smart_pos_order_id = http.request.env['smart.pos.order'].create(vals)
        if not smart_pos_order_id:
            data_return =  {
                "err": True,
                "message": "POS Order Created Eror",
                "data": {}      
            }
        else:
            data_return =  {
                "err": False,
                "message": "POS Order Created",
                "data": {
                    "id": smart_pos_order_id.id
                }      
            }
        return data_return


    @validate_token
    @http.route("/api/smartpos/v1.0/closepossession", type="json", auth="none", methods=["POST"], csrf=False)
    def pos_close_pos_session(self, **post):
        pass

    @validate_token
    @http.route("/api/smartpos/v1.0/sync_pos_config", type="json", auth="none", methods=["POST"], csrf=False)
    def pos_sync_product(self, **post):
        #Sync Product
        pos_config_ds = http.request.env['product.product'].sudo().search([('is_avaiable_on_pos','=',True)])
        return  json.dumps(product_product_ids.read(['name','barcode','default_code','lst_price','standard_price']))
    
    @validate_token
    @http.route("/api/smartpos/v1.0/sync_pos_product_category", type="json", auth="none", methods=["POST"], csrf=False)
    def pos_sync_smart_pos_product_category(self, **post):
        #Sync Pos Product Category
        product_product_ids = http.request.env['smart.pos.product.category'].sudo().search([])
        return  json.dumps(product_product_ids.read(['name']))
    
    @validate_token
    @http.route("/api/smartpos/v1.0/sync_product", type="json", auth="none", methods=["POST"], csrf=False)
    def pos_sync_product(self, **post):
        #Sync Product
        product_product_ids = http.request.env['product.product'].sudo().search([('is_avaiable_on_pos','=',True)])
        return  json.dumps(product_product_ids.read(['name','barcode','default_code','lst_price','standard_price']))
    

    @validate_token
    @http.route("/api/smartpos/v1.0/sync_partner", type="json", auth="none", methods=["POST"], csrf=False)
    def pos_sync_partner(self, **post):
        #Sync Partner
        product_product_ids = http.request.env['res.partner'].sudo().search([])
        return  json.dumps(product_product_ids.read(['name']))

    


    
    
    