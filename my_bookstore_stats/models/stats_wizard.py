from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class BookstoreStatsWizard(models.TransientModel):
    """
    Model Wizard này không lưu dữ liệu vĩnh viễn.
    Nó chỉ dùng để tính toán và hiển thị dữ liệu tạm thời.
    """
    _name = 'bookstore.stats.wizard'
    _description = 'Bookstore Statistics Wizard'

    # Các trường để hiển thị kết quả
    total_books = fields.Integer('Tổng số sách', readonly=True)
    average_age = fields.Float('Tuổi sách trung bình', readonly=True)
    oldest_book_id = fields.Many2one(
        'bookstore.book',
        string='Sách cũ nhất',
        readonly=True
    )
    author_stats_display = fields.Text('Thống kê tác giả', readonly=True)

    @api.model
    def default_get(self, fields_list):
        # Gọi hàm default_get gốc
        res = super(BookstoreStatsWizard, self).default_get(fields_list)

        # 1. LẤY DỮ LIỆU
        # Lấy tất cả dữ liệu sách dưới dạng LIST CỦA DICTIONARIES
        # Đây là một "Data Manipulation Pattern" cơ bản
        books_data = self.env['bookstore.book'].search_read(
            [], ['id', 'author', 'age']
        )

        # Nếu không có sách, trả về luôn
        if not books_data:
            res['author_stats_display'] = 'Chưa có sách để thống kê.'
            res['total_books'] = 0
            return res

        _logger.info(f"Dữ liệu sách thô (List of Dicts): {books_data}")

        # --- ÁP DỤNG CÁC KHÁI NIỆM ---

        # 2. WORKING WITH DICTIONARIES (Data Manipulation Pattern)
        # Mục tiêu: Đếm số sách của mỗi tác giả
        # Chúng ta dùng "frequency map" (bản đồ tần suất), 1 pattern phổ biến
        author_counts = {}
        for book in books_data:
            # Dùng dict.get() để lấy 'author', nếu không có thì dùng 'Unknown'
            author = book.get('author') or 'Unknown'
            # Dùng dict.get(key, 0) + 1 để tăng bộ đếm
            author_counts[author] = author_counts.get(author, 0) + 1

        _logger.info(f"Thống kê tác giả (Dict): {author_counts}")

        # 3. LAMBDA FUNCTIONS & FUNCTIONAL PROGRAMMING (map, filter)
        # Mục tiêu: Tính tuổi trung bình

        # 3a. Dùng map() và lambda để trích xuất list các tuổi (age)
        all_ages = list(map(lambda b: b['age'], books_data))

        # 3b. Dùng filter() và lambda để loại bỏ các sách có tuổi = 0 (sách mới)
        valid_ages = list(filter(lambda age: age > 0, all_ages))

        avg_age = 0.0
        if valid_ages:
            avg_age = sum(valid_ages) / len(valid_ages)

        # 3c. (Bonus) Dùng max() với lambda key để tìm sách cũ nhất
        # 'max()' cũng là một dạng functional programming
        oldest_book_dict = max(books_data, key=lambda b: b['age'])
        oldest_book_id = oldest_book_dict['id']

        # 4. LIST COMPREHENSIONS
        # Mục tiêu: Chuyển dict 'author_counts' thành một chuỗi (string) đẹp
        # (VD: {'Tác giả A': 2, 'Tác giả B': 1})
        stats_lines = [
            f"- {author}: {count} cuốn"
            for author, count in author_counts.items()
        ]

        # .join() cũng là một "Data Manipulation Pattern"
        author_display_str = "\n".join(stats_lines)

        # 5. GÁN KẾT QUẢ
        # Gán các giá trị đã tính toán vào 'res' để wizard hiển thị
        res['total_books'] = len(books_data)
        res['average_age'] = round(avg_age, 2)
        res['oldest_book_id'] = oldest_book_id
        res['author_stats_display'] = author_display_str

        _logger.info("Hoàn thành tính toán thống kê!")

        return res