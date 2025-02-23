from fastapi.testclient import TestClient
from main import app, purchases, Purchase  
from datetime import date
import io
import csv


client = TestClient(app)


def create_csv_file(data):

    csv_file = io.StringIO()
    writer = csv.DictWriter(csv_file, fieldnames=["customer_name", "country", "purchase_date", "amount"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    csv_file.seek(0)

    return io.BytesIO(csv_file.getvalue().encode("utf-8"))


test_purchase = {
    "customer_name": "John Doe",
    "country": "USA",
    "purchase_date": "2023-10-01",
    "amount": 100.0
}

test_bulk_data = [
    {"customer_name": "Alice", "country": "UK", "purchase_date": "2023-10-02", "amount": "200.0"},
    {"customer_name": "Bob", "country": "USA", "purchase_date": "2023-10-03", "amount": "150.0"}
]


def test_add_purchase():
   
    response = client.post("/purchase/", json=test_purchase)
    assert response.status_code == 200
    assert response.json() == test_purchase

def test_add_bulk_purchases():

    csv_file = create_csv_file(test_bulk_data)


    response = client.post("/purchase/bulk/", files={"file": ("test.csv", csv_file, "text/csv")})

    
    assert response.status_code == 200
    assert response.json() == {"added": len(test_bulk_data)}

def test_get_purchases():
 
    purchases.clear()
    purchases.extend([
        Purchase(customer_name="John Doe", country="USA", purchase_date=date(2023, 10, 1), amount=100.0),
        Purchase(customer_name="Alice", country="UK", purchase_date=date(2023, 10, 2), amount=200.0),
        Purchase(customer_name="Bob", country="USA", purchase_date=date(2023, 10, 3), amount=150.0)
    ])


    response = client.get("/purchase/purchases/", params={"country": "USA"})
    assert response.status_code == 200
    assert len(response.json()) == 2  


    response = client.get("/purchase/purchases/", params={"start_date": "2023-10-02"})
    assert response.status_code == 200
    assert len(response.json()) == 2 


    response = client.get("/purchase/purchases/", params={"country": "USA", "start_date": "2023-10-03"})
    assert response.status_code == 200
    assert len(response.json()) == 1 

def test_invalid_csv_upload():

    invalid_csv = io.BytesIO(b"invalid,data\n1,2,3,4")
    response = client.post("/purchase/bulk/", files={"file": ("invalid.csv", invalid_csv, "text/csv")})

   
    assert response.status_code == 400
    assert "Error processing row" in response.json()["detail"]

def test_invalid_purchase_data():

    invalid_purchase = {
        "customer_name": "John Doe",
        "country": "USA",
        "purchase_date": "invalid-date",  
        "amount": 100.0
    }
    response = client.post("/purchase/", json=invalid_purchase)
    assert response.status_code == 422  