from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import date
from typing import Optional, List
import io
import csv

app = FastAPI(title="Customer Purchases API")

# In-memory storage
purchases = []

class Purchase(BaseModel):
    customer_name: str
    country: str
    purchase_date: date
    amount: float

@app.post("/purchase/", response_model=Purchase)
async def add_purchase(purchase: Purchase):
    purchases.append(purchase)
    return purchase

@app.post("/purchase/bulk/")
async def add_bulk_purchases(file: UploadFile = File(...)):
    if file.content_type not in ["text/csv"]:
        raise HTTPException(status_code=400, detail="Invalid file format")
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))
    new_purchases = []
    for row in reader:
        try:
            purchase = Purchase(
                customer_name=row["customer_name"],
                country=row["country"],
                purchase_date=date.fromisoformat(row["purchase_date"]),
                amount=float(row["amount"])
            )
            purchases.append(purchase)
            new_purchases.append(purchase)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing row: {row} - {e}")
    return JSONResponse(content={"added": len(new_purchases)})


@app.get("/purchase/purchases/", response_model=List[Purchase])
def get_purchases(country: Optional[str] = None, start_date: Optional[date] = None):
    filtered = purchases
    if country:
        filtered = [p for p in filtered if p.country.lower() == country.lower()]
    if start_date:
        filtered = [p for p in filtered if p.purchase_date >= start_date]
    return filtered


