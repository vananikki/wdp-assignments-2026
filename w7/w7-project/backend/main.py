from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================================
# Pydantic Models for Items CRUD
# ========================================================

class ItemCreate(BaseModel):
    name: str
    price: float
    in_stock: bool = True

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    in_stock: bool | None = None

class ItemPublic(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

class ItemListResponse(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int


# ========================================================
# In-Memory Storage
# ========================================================

items_db: list[dict] = []
next_id: int = 1


# ========================================================
# Endpoints: Items CRUD
# ========================================================

# Part B & Part D: GET /items with Filtering, Sorting & Envelope Response
@app.get("/items", response_model=ItemListResponse, status_code=200)
def list_items(
    min_price: float | None = None,
    max_price: float | None = None,
    q: str | None = Query(None, min_length=2),
    sort_by: str = Query("id", pattern="^(id|name|price)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1)
):
    results = items_db

    # 1. Filtering
    if min_price is not None:
        results = [item for item in results if item["price"] >= min_price]

    if max_price is not None:
        results = [item for item in results if item["price"] <= max_price]

    if q is not None:
        q_lower = q.lower()
        results = [item for item in results if q_lower in item["name"].lower()]

    # 2. Sorting
    is_reverse = (order == "desc")
    results = sorted(results, key=lambda x: x[sort_by], reverse=is_reverse)

    # 3. Total count before pagination slicing
    total = len(results)

    # 4. Slicing / Pagination
    paginated_items = results[skip : skip + limit]

    return {
        "items": paginated_items,
        "total": total,
        "skip": skip,
        "limit": limit
    }


# GET /items/{id}
@app.get("/items/{item_id}", response_model=ItemPublic, status_code=200)
def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


# Part C: POST /items with Duplicate Name Check (409 Conflict)
@app.post("/items", response_model=ItemPublic, status_code=201)
def create_item(item_data: ItemCreate):
    global next_id

    # Check duplicate name (case-insensitive)
    for existing in items_db:
        if existing["name"].lower() == item_data.name.lower():
            raise HTTPException(status_code=409, detail="Item with this name already exists")

    new_item = {
        "id": next_id,
        "name": item_data.name,
        "price": item_data.price,
        "in_stock": item_data.in_stock
    }
    items_db.append(new_item)
    next_id += 1
    return new_item


# PUT /items/{id} with Duplicate Name Check
@app.put("/items/{item_id}", response_model=ItemPublic, status_code=200)
def update_item(item_id: int, item_data: ItemCreate):
    target_index = None
    target_item = None

    for index, item in enumerate(items_db):
        if item["id"] == item_id:
            target_index = index
            target_item = item
            break

    if target_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Only check duplicate if name is changing
    if target_item["name"].lower() != item_data.name.lower():
        for existing in items_db:
            if existing["id"] != item_id and existing["name"].lower() == item_data.name.lower():
                raise HTTPException(status_code=409, detail="Item with this name already exists")

    updated_item = {
        "id": item_id,
        "name": item_data.name,
        "price": item_data.price,
        "in_stock": item_data.in_stock
    }
    items_db[target_index] = updated_item
    return updated_item


# Part A: PATCH /items/{id} Partial Update with Duplicate Name Check
@app.patch("/items/{item_id}", response_model=ItemPublic, status_code=200)
def partial_update_item(item_id: int, patch_data: ItemUpdate):
    target_item = None
    for item in items_db:
        if item["id"] == item_id:
            target_item = item
            break

    if target_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    update_dict = patch_data.model_dump(exclude_unset=True)

    # Check duplicate name if 'name' was provided and actually changed
    if "name" in update_dict and update_dict["name"].lower() != target_item["name"].lower():
        for existing in items_db:
            if existing["id"] != item_id and existing["name"].lower() == update_dict["name"].lower():
                raise HTTPException(status_code=409, detail="Item with this name already exists")

    # Update only provided fields
    for key, value in update_dict.items():
        target_item[key] = value

    return target_item


# DELETE /items/{id}
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    for index, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Item not found")


# ========================================================
# Part E — DS-AI Track: POST /predict/house-price
# ========================================================

class HousePriceRequest(BaseModel):
    area_sqm: float = Field(..., gt=0, description="Area must be greater than 0")
    bedrooms: int = Field(..., ge=0, description="Bedrooms must be non-negative")
    distance_to_center_km: float = Field(..., ge=0)

class HousePricePrediction(BaseModel):
    predicted_price: float
    currency: str = "VND"

@app.post("/predict/house-price", response_model=HousePricePrediction, status_code=200)
def predict_house_price(req: HousePriceRequest):
    price = (
        req.area_sqm * 15_000_000
        - req.distance_to_center_km * 5_000_000
        + req.bedrooms * 20_000_000
    )
    return {
        "predicted_price": max(0.0, float(price)),
        "currency": "VND"
    }


# ========================================================
# Legacy Endpoints from Week 7 (Maintained for house_form.html)
# ========================================================

def predict_price(area: float, bedrooms: int, location: str) -> float:
    price = 500_000_000
    price += 15_000_000 * area
    price += 50_000_000 * bedrooms

    location = location.lower()
    if location == "hanoi":
        price *= 1.3
    elif location == "hcmc":
        price *= 1.25

    return round(price / 1_000_000) * 1_000_000

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

app.mount(
    "/static",
    StaticFiles(directory="../frontend"),
    name="static"
)