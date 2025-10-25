{
    'name': 'Bookstore test API Odoo',  # Tên module
    'version': '1.0',
    'summary': 'Module đơn giản để quản lý sách và test API Odoo',
    'author': 'Baao',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/bookstore_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}