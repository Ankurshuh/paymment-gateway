from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
from pydantic import BaseModel
import razorpay


router = APIRouter(prefix="/api/payments", tags=["Payments"])

client = razorpay.Client(auth=("KEY_ID", "KEY_SECRET"))


client = MongoClient("mongodb+srv://ankurshukla123:iZyUoUrhWsrgpAHh@cluster0.dt0junk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["payment_gateway"]
transactions = db["ankur"]

class PaymentRequest(BaseModel):
    user_id: str 
    amount: float
    description: str

class PaymentResponse(BaseModel):
    transaction_id: str
    status: str
    amount: float
    timestamp: datetime

class OrderRequest(BaseModel):
    amount: int  
    currency: str = "INR"

@router.post("/create-order")
def create_order(order: OrderRequest):
    razorpay_order = client.order.create({
        "amount": order.amount,
        "currency": order.currency,
        "payment_capture": 1
    })
    return razorpay_order

@router.post("/create", response_model=PaymentResponse)
def create_payment(payment: PaymentRequest):
    # simulate payment (could integrate with Stripe/Razorpay)
    transaction = {
        "user_id": payment.user_id,
        "amount": payment.amount,
        "description": payment.description,
        "status": "SUCCESS" if payment.amount > 0 else "FAILED",
        "timestamp": datetime.utcnow()
    }
    result = transactions.insert_one(transaction)
    
    return PaymentResponse(
        transaction_id=str(result.inserted_id),
        status=transaction["status"],
        amount=transaction["amount"],
        timestamp=transaction["timestamp"]
    )

@router.get("/{transaction_id}")
def get_payment(transaction_id: str):
    tx = transactions.find_one({"_id": ObjectId(transaction_id)})
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    tx["_id"] = str(tx["_id"])
    return tx
