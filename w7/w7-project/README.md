# FastAPI Lab: Advanced CRUD & ML Prediction Endpoint

Dự án mở rộng API xây dựng bằng **FastAPI** và **Pydantic v2**, bao gồm các kỹ thuật nâng cao trong thiết kế RESTful API (Partial Update, Filtering, Sorting, Pagination Envelope, Conflict Handling) và tích hợp endpoint dự đoán giá nhà cho track DS/AI.

## 📌 Nội dung triển khai

| Phần | Tính năng | Mô tả chi tiết |
| --- | --- | --- |
| **Part A** | **Partial Updates (PATCH)** | Dùng model `ItemUpdate` với `model_dump(exclude_unset=True)` để chỉ cập nhật những field client gửi lên, giữ nguyên các field còn lại. |
| **Part B** | **Filtering, Searching & Sorting** | Lọc theo khoảng giá (`min_price`, `max_price`), tìm kiếm chuỗi con không phân biệt hoa thường (`q`), sắp xếp (`sort_by`, `order`) trước khi cắt lát phân trang. |
| **Part C** | **409 Conflict Handling** | Bắt lỗi trùng lặp tên item (case-insensitive) khi tạo mới (`POST`) hoặc đổi tên (`PUT`/`PATCH`), trả về HTTP `409 Conflict`. |
| **Part D** | **Envelope Response Pattern** | Chuẩn hóa response của `GET /items` theo dạng envelope: `{ items, total, skip, limit }`, trong đó `total` là số bản ghi khớp sau khi lọc. |
| **Part E** | **Toy ML Prediction Endpoint** | Cung cấp endpoint `POST /predict/house-price` với request body validation sử dụng `Field(gt=0)` và `Field(ge=0)`, tự động trả về `422` nếu dữ liệu không hợp lệ. |

## 🛠️ Cấu trúc thư mục

```text
.
├── backend/
│   └── main.py          # File mã nguồn FastAPI chứa toàn bộ router và schema
├── frontend/
│   └── house_form.html  # Giao diện frontend dự đoán giá nhà
└── README.md            # Tài liệu hướng dẫn sử dụng và kiểm thử
```

## 🚀 Hướng dẫn cài đặt & Chạy ứng dụng

### 1. Cài đặt thư viện phụ thuộc

Yêu cầu Python 3.10+:

```bash
pip install fastapi uvicorn pydantic
```

### 2. Khởi chạy server

Di chuyển vào thư mục `backend/` và khởi chạy server:

```bash
cd backend
uvicorn main:app --reload
```

* **API Docs (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **API Redoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📖 Chi tiết Endpoints

### 1. Quản lý Items

#### `GET /items`
Lấy danh sách sản phẩm theo bộ lọc, sắp xếp và phân trang (Envelope pattern).

* **Query Params:**
  * `min_price` *(float, optional)*: Giá nhỏ nhất.
  * `max_price` *(float, optional)*: Giá lớn nhất.
  * `q` *(string, optional, min_length=2)*: Từ khóa tìm kiếm theo tên.
  * `sort_by` *(string, default="id", regex: `^(id|name|price)$`)*: Trường sắp xếp.
  * `order` *(string, default="asc", regex: `^(asc|desc)$`)*: Hướng sắp xếp (`asc` / `desc`).
  * `skip` *(int, default=0, ge=0)*: Vị trí bắt đầu.
  * `limit` *(int, default=10, ge=1)*: Số lượng bản ghi mỗi trang.

* **Response `200 OK`:**
  ```json
  {
    "items": [
      { "id": 1, "name": "Bàn phím", "price": 450000.0, "in_stock": true }
    ],
    "total": 1,
    "skip": 0,
    "limit": 10
  }
  ```

#### `POST /items`
Tạo mới sản phẩm (Tự động kiểm tra trùng tên).

* **Request Body:**
  ```json
  {
    "name": "Bàn phím cơ",
    "price": 750000,
    "in_stock": true
  }
  ```
* **Responses:**
  * `201 Created`: Tạo thành công.
  * `409 Conflict`: Tên item đã tồn tại.

#### `PATCH /items/{item_id}`
Cập nhật một phần thuộc tính của sản phẩm.

* **Request Body (chỉ gửi trường muốn sửa):**
  ```json
  {
    "price": 690000
  }
  ```
* **Responses:**
  * `200 OK`: Cập nhật thành công.
  * `404 Not Found`: Không tìm thấy item.
  * `409 Conflict`: Tên mới bị trùng với item khác.

### 2. Prediction Endpoints

#### `POST /predict/house-price` (Part E - DS/AI Track)
Dự đoán giá nhà dựa trên diện tích, khoảng cách tới trung tâm và số phòng ngủ.

* **Request Body:**
  ```json
  {
    "area_sqm": 85.5,
    "bedrooms": 3,
    "distance_to_center_km": 4.2
  }
  ```
* **Responses:**
  * `200 OK`:
    ```json
    {
      "predicted_price": 1321500000.0,
      "currency": "VND"
    }
    ```
  * `422 Unprocessable Entity`: Trả về khi `area_sqm <= 0` hoặc `bedrooms < 0` nhờ Pydantic `Field`.

#### `GET /predict` (Legacy Endpoint)
Duy trì tương thích với giao diện `frontend/house_form.html`.

## 🧪 Ví dụ kiểm thử với cURL

```bash
# 1. Tạo mới item
curl -X POST "http://127.0.0.1:8000/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Laptop Dell", "price": 15000000}'

# 2. Thử tạo trùng tên (Kiểm tra lỗi 409 Conflict)
curl -X POST "http://127.0.0.1:8000/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "laptop dell", "price": 16000000}'

# 3. Cập nhật một phần giá sản phẩm (PATCH)
curl -X PATCH "http://127.0.0.1:8000/items/1" \
     -H "Content-Type: application/json" \
     -d '{"price": 14500000}'

# 4. Lọc, tìm kiếm, sắp xếp và kiểm tra Envelope pattern
curl "http://127.0.0.1:8000/items?q=lap&min_price=10000000&sort_by=price&order=desc&skip=0&limit=5"

# 5. Test validation Part E (Dữ liệu không hợp lệ trả về 422)
curl -X POST "http://127.0.0.1:8000/predict/house-price" \
     -H "Content-Type: application/json" \
     -d '{"area_sqm": -10, "bedrooms": 2, "distance_to_center_km": 3}'
```