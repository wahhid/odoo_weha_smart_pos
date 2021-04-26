# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import content_disposition, request
import logging


_logger = logging.getLogger(__name__)


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
        pass

    

    