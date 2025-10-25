from odoo import models, api, fields
from datetime import date

from odoo.release import author


class BookstoreBook(models.Model):
    _name = 'bookstore.book'
    _description = 'Model book bookstore'

    name = fields.Char('Tên sách', required=True)
    author = fields.Char('Tên tác giả')
    publication_year = fields.Integer('Năm xuất bản')
    publisher = fields.Char('Nhà xuất bản')

    # Test depend
    age = fields.Integer(
        'Tuổi sách (năm)',
        compute='_compute_age',
        store=True
    )

    description = fields.Text('Mô tả')

    @api.depends('publication_year')
    def _compute_age(self):
        current_year = date.today().year
        for book in self:
            if book.publication_year > 0:
                book.age = current_year - book.publication_year
            else:
                book.age = 0

    @api.onchange('author')
    def _onchange_author(self):
        for record in self:
            name = record.name or ''
            author = record.author or ''
            record.description = f"{name} - {author}"

    @api.model #In hoa tên sách, title author
    def create(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].upper()

        if 'author' in vals and vals['author']:
            vals['author'] = vals['author'].title()

        new_record = super(BookstoreBook, self).create(vals)

        return new_record
