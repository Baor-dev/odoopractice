{
    'name': 'My Bookstore Statistics',
    'version': '1.0',
    'summary': 'Phân tích thống kê sách sử dụng các kỹ thuật Python nâng cao.',
    'author': 'Baobao',
    'license': 'LGPL-3',
    'depends': [
        'my_bookstore',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stats_wizard_views.xml',
    ],
    'installable': True,
}