## Tóm tắt kiến thức

### 1. Cơ chế `_inherit = 'model_cha'`

- Giống như việc **mở rộng hoặc sửa đổi trực tiếp** model cha.  
- Khi cài đặt module, **Odoo sẽ thêm các cột mới** vào **bảng CSDL của model cha** đã tồn tại.  
- **Tất cả dữ liệu nằm chung trong một bảng.**

---

### 2. Cơ chế `_inherits = {'model_cha': 'khoa_ngoai'}`

- Hoạt động theo kiểu **ủy quyền (delegation)**.  
- Khi cài đặt module, **Odoo sẽ tạo một bảng CSDL mới hoàn toàn** cho model con.  
- Khi tạo một bản ghi mới cho model con:
  - Odoo sẽ thêm **một hàng mới vào bảng CSDL của model con**,  
  - Đồng thời **tự động tạo một hàng mới tương ứng trong bảng CSDL của model cha**,  
  - Cuối cùng **liên kết hai hàng này** thông qua **trường khóa ngoại** đã định nghĩa.  
- **Dữ liệu được lưu trữ ở hai bảng riêng biệt nhưng có liên kết chặt chẽ.**
