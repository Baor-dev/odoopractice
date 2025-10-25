# -*- coding: utf-8 -*-
from odoo import models, fields

class DemoCustomer(models.Model):
    _name = 'demo.customer'
    _description = 'Demo Customer (inherits Human)'

    # --- Kế thừa Delegation (_inherits) ---
    _inherits = {'demo.human': 'human_id'}

    # --- Trường liên kết  ---
    human_id = fields.Many2one(
        'demo.human',
        string='Related Human',
        required=True,
        ondelete='cascade',
        index=True,
        help="Liên kết đến bản ghi Human chứa thông tin cơ bản."
    )

    # --- Các trường riêng của Customer ---
    customer_rank = fields.Integer(string='Hạng Khách Hàng', tracking=True)
    registration_date = fields.Date(string='Ngày Đăng Ký', default=fields.Date.today)
