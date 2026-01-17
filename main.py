from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route import payments

app = FastAPI(title="Payment Gateway API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.include_router(payments.router)
