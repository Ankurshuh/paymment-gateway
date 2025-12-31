import React, { useState } from "react";
import "./App.css";
import axios from "axios";

const loadRazorpay = () => {
  return new Promise((resolve) => {
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.onload = () => resolve(true);
    document.body.appendChild(script);
  });
};

const payNow = async () => {
  await loadRazorpay();

  const res = await axios.post("http://localhost:8000/create-order", {
    amount: 50000 // ₹500
  });

  const options = {
    key: "RAZORPAY_KEY_ID",
    amount: res.data.amount,
    currency: "INR",
    order_id: res.data.id,
    handler: function (response) {
      alert("Payment Successful!");
      console.log(response);
    }
  };

  const rzp = new window.Razorpay(options);
  rzp.open();
};

export default function PaymentForm() {
  const [amount, setAmount] = useState("");
  const [userId, setUserId] = useState("");
  const [description, setDescription] = useState("");
  const [message, setMessage] = useState("");

  const handlePayment = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8000/api/payments/create", {
        user_id: userId,
        amount: parseFloat(amount),
        description,
      });
      setMessage(`Transaction ${res.data.status}! ID: ${res.data.transaction_id}`);
    } catch (err) {
      setMessage("Payment failed!");
    }
  };

  return (
    <div id="payment-container">
      <h2>Make a Payment</h2>
      <form className="aa" onSubmit={handlePayment}>
        <input  type="text" placeholder="User ID" value={userId} onChange={(e) => setUserId(e.target.value)} required />
        <input type="number" placeholder="Amount" value={amount} onChange={(e) => setAmount(e.target.value)} required />
        <input type="text" placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
        <button  type="submit">Pay Now</button>
      </form>
      <p>{message}</p>
    </div>
  );
}
