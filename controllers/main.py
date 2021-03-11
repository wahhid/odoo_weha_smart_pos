# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import content_disposition, request
import logging


_logger = logging.getLogger(__name__)


class WehaSmartPosController(http.Controller):
    @http.route(['/weha_pos/pos',], type='http', auth="user", csrf=False)
    def pos(self,**args):
        return http.request.render('odoo_weha_smart_pos.pos_screen',{})
    