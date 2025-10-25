# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DemoHuman(models.Model):
    _name = 'demo.human'
    _description = 'Demo Human Base Model'

    name = fields.Char(string='Họ và Tên', required=True)
    birth_date = fields.Date(string='Ngày Sinh')
    gender = fields.Char(string='Gender')


