from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

# We use def because this endpoint does not perform asynchronous I/O.
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