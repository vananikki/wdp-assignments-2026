from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================================
# Lab 1: Models & In-Memory Storage for Items CRUD
# ========================================================

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

class ItemResponse(Item):
    id: int

# Danh sách lưu tạm trong RAM
items_db: list[dict] = []
next_id: int = 1


# ========================================================
# Lab 1 Endpoints: GET, POST, PUT, DELETE /items
# ========================================================

# 1. GET /items: Lấy toàn bộ danh sách items
@app.get("/items", response_model=list[ItemResponse], status_code=200)
def get_all_items():
    return items_db


# 2. GET /items/{id}: Lấy chi tiết một item theo id
@app.get("/items/{item_id}", response_model=ItemResponse, status_code=200)
def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


# 3. POST /items: Tạo mới một item
@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item_data: Item):
    global next_id
    new_item = {
        "id": next_id,
        "name": item_data.name,
        "price": item_data.price,
        "in_stock": item_data.in_stock
    }
    items_db.append(new_item)
    next_id += 1
    return new_item


# 4. PUT /items/{id}: Cập nhật thông tin item
@app.put("/items/{item_id}", response_model=ItemResponse, status_code=200)
def update_item(item_id: int, item_data: Item):
    for index, item in enumerate(items_db):
        if item["id"] == item_id:
            updated_item = {
                "id": item_id,
                "name": item_data.name,
                "price": item_data.price,
                "in_stock": item_data.in_stock
            }
            items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


# 5. DELETE /items/{id}: Xóa một item
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    for index, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Item not found")


# =========================
# Task 1: Prediction function
# =========================

def predict_price(area: float, bedrooms: int, location: str) -> float:
    price = 500_000_000

    price += 15_000_000 * area
    price += 50_000_000 * bedrooms

    location = location.lower()

    if location == "hanoi":
        price *= 1.3
    elif location == "hcmc":
        price *= 1.25

    # Round to the nearest million VND
    price = round(price / 1_000_000) * 1_000_000

    return price


# Test Task 1
print(predict_price(80, 3, "hanoi"))


# =========================
# Task 2: GET /predict
# =========================

@app.get("/predict")
def predict(
    area: float,
    bedrooms: int,
    location: str = "other"
):
    predicted_price = predict_price(area, bedrooms, location)

    return {
        "area": area,
        "bedrooms": bedrooms,
        "location": location,
        "predicted_price": predicted_price
    }


# =========================
# Task 4: Serve frontend
# =========================

app.mount(
    "/static",
    StaticFiles(directory="../frontend"),
    name="static"
)
