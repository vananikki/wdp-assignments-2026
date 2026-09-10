# Week 6 – House Price Prediction API

## How to Run

Open a terminal in the `backend/` folder and activate the virtual environment if needed. Then start FastAPI:

```bash
uvicorn main:app --reload
```

Open the Swagger UI at:

```text
http://127.0.0.1:8000/docs
```

The frontend is served directly by FastAPI. Open it at:

```text
http://127.0.0.1:8000/static/house_form.html
```

The frontend uses JavaScript `fetch()` to call the `GET /predict` endpoint and display the predicted house price.

## Task 3 – Explain Why

### Why does `/predict` still work when `location` is omitted?

`location` is an optional query parameter with a default value of `"other"`. Therefore, if the client does not provide `location`, FastAPI automatically uses `"other"`.

For example:

```text
/predict?area=80&bedrooms=3
```

is valid and uses:

```text
location = "other"
```

### Why does `/predict` return a 422 error when `area` is omitted?

`area` is a required query parameter because the endpoint defines it as a required `float` parameter. FastAPI validates the incoming request automatically. If `area` is missing, FastAPI cannot provide the required value, so it returns HTTP status `422 Unprocessable Entity`.

## Task 3 – Test Result

For:

```text
area=80
bedrooms=3
location=hanoi
```

the returned JSON is:

```json
{
    "area": 80.0,
    "bedrooms": 3,
    "location": "hanoi",
    "predicted_price": 2405000000.0
}
```

The calculation is:

```text
500,000,000
+ 80 × 15,000,000
+ 3 × 50,000,000
= 1,850,000,000

Hanoi multiplier:
1,850,000,000 × 1.3
= 2,405,000,000 VND
```

## Task 5 – Why Does a Relative URL Work?

The JavaScript uses:

```javascript
fetch(`/predict?area=${area}&bedrooms=${bedrooms}&location=${location}`)
```

A relative URL works because the frontend page and the FastAPI API are served from the same origin:

```text
http://127.0.0.1:8000
```

The frontend is loaded from:

```text
http://127.0.0.1:8000/static/house_form.html
```

Therefore, the browser resolves:

```text
/predict
```

to:

```text
http://127.0.0.1:8000/predict
```

Both the frontend and backend use the same protocol, hostname, and port, so this is a same-origin request and no CORS configuration is needed.

This is why we should use the relative URL `/predict` instead of an absolute URL such as `http://127.0.0.1:8000/predict`.

## Task 6 – Bonus

An optional `POST /predict` endpoint can accept the house information as a JSON request body using a Pydantic model.

The main difference is that `GET /predict` sends data through query parameters, while `POST /predict` sends data inside a JSON request body.
