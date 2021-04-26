import re
import ast
import functools
from datetime import datetime, date
import logging
import json
import werkzeug.wrappers
from odoo.exceptions import AccessError
from odoo.addons.weha_smart_pos.common import invalid_response, valid_response

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
        data = json.loads(request.httprequest.data)
        _logger.info(data)
        return 'Success'

    @validate_token
    @http.route("/api/smartpos/v1.0/createpossession", type="json", auth="none", methods=["POST"], csrf=False)
    def pos_create_pos_session(self, **post):
        pass

    @validate_token
    @http.route("/api/smartpos/v1.0/createposorder", type="json", auth="none", methods=["POST"], csrf=False)
    def pos_create_pos_order(self, **post):
        pass

    @validate_token
    @http.route("/api/smartpos/v1.0/closepossession", type="json", auth="none", methods=["POST"], csrf=False)
    def pos_close_pos_session(self, **post):
        pass

    @validate_token
    @http.route("/api/smartpos/v1.0/sync_product", type="json", auth="none", methods=["POST"], csrf=False)
    def pos_sync_product(self, **post):
        #Sync Product and Pos Product Category
        product_product_ids = http.request.env['product.product'].sudo().search([])
        _logger.info(product_product_ids.read(['name','barcode','default_code','lst_price','standard_price']))
        products = json.dumps(product_product_ids.read(['name','barcode','default_code','lst_price','standard_price']))
        result = products.replace("\\", "") 
        return result
    

    