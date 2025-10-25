# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class DemoSuperhuman(models.Model):
    _inherit = 'demo.human'
    _description = 'Demo Superhuman (Linked to Human)'

    # --- Các trường riêng của Superhuman ---
    superpower = fields.Char(string='Siêu năng lực', required=True, tracking=True)
    hero_name = fields.Char(string='Bí danh Siêu anh hùng', tracking=True)



