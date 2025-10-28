import io
import csv
from odoo import http
from odoo.http import request, Response
from werkzeug.urls import url_join


class BookExportController(http.Controller):

    @http.route('/bookstore/utils', type='http', auth='user', website=False)
    def show_utils_page(self, **kw):
        """
        Route này tạo 1 trang HTML đơn giản
        với 1 link để tải CSV.
        """
        # Dùng ORM để đếm sách cho vui
        book_count = request.env['bookstore.book'].search_count([])

        # --- VẬN DỤNG WERKZEUG ---
        base_url = request.httprequest.url_root
        # Dùng tiện ích url_join của Werkzeug để tạo URL an toàn
        download_url = url_join(base_url, '/bookstore/export_csv')

        html_body = f"""
            <h1>Bookstore Utilities</h1>
            <p>Chúng ta đang có {book_count} cuốn sách trong database.</p>
            <a href="{download_url}" class="btn btn-primary">
                Tải Báo cáo CSV (Dùng Raw SQL - Psycopg2)
            </a>
        """

        # 'request.make_response' tạo 1 đối tượng Response của Werkzeug
        return request.make_response(
            html_body,
            headers=[('Content-Type', 'text/html; charset=utf-8')]
        )

    # --- VẬN DỤNG PSYCOPG2 ---
    @http.route('/bookstore/export_csv', type='http', auth='user')
    def export_books_csv(self, **kw):
        """
        Route này sẽ thực thi SQL thô (psycopg2)
        và trả về 1 file CSV.
        """

        # 1. Lấy cursor của psycopg2
        # 'request.env.cr' CHÍNH LÀ 1 đối tượng cursor của psycopg2
        cr = request.env.cr

        # 2. Viết câu lệnh SQL thô
        sql_query = "SELECT name, author, publication_year FROM bookstore_book ORDER BY name"

        results = []
        try:
            # 3. Thực thi (execute) - Đây là hàm của psycopg2
            cr.execute(sql_query)

            # 4. Lấy tất cả kết quả (fetchall) - Đây là hàm của psycopg2
            results = cr.fetchall()

        except Exception as e:
            # Nếu lỗi, nó sẽ là một 'psycopg2.Error'
            return request.make_response(f"Lỗi SQL (Psycopg2): {e}")

        # 5. Dùng 'io' để tạo file CSV trong bộ nhớ
        output = io.StringIO()
        output.write('\ufeff')
        writer = csv.writer(output)

        # Ghi hàng tiêu đề
        writer.writerow(['Tên sách', 'Tác giả', 'Năm XB'])
        # Ghi dữ liệu (results là 1 list các tuple, vd: [('Sách A', 'Tác giả B', 2005), ...])
        writer.writerows(results)

        csv_data = output.getvalue()
        output.close()

        # 6. Dùng http.Response (dựa trên Werkzeug) để trả về file
        # Báo cho trình duyệt biết đây là 1 file CSV để tải về
        return request.make_response(
            csv_data,
            headers=[
                ('Content-Type', 'text/csv; charset=utf-8'),
                ('Content-Disposition', 'attachment; filename="book_export.csv"')
            ]
        )