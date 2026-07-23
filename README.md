# 🚀 Business Automation using Multi-Agent System

An AI-powered Business Automation System that helps businesses efficiently manage inventory, billing, procurement, customers, staff, finance, and business analytics using multiple intelligent agents.

---

## 📌 Overview

This project is a complete business management solution developed using FastAPI and Streamlit. It automates routine business operations while providing intelligent insights through AI-powered agents.

The system supports multiple businesses, ensuring complete data isolation using `business_id`, making it suitable for SaaS-based deployment.

---

## ✨ Features

### 🏢 Business Management
- Business Registration
- Secure Login & Authentication
- Multi-Business Support
- Role-Based Access (Admin & Staff)

### 📦 Inventory Management
- Add/Edit/Delete Products
- Inventory Tracking
- Low Stock Detection
- Inventory Value Calculation

### 👥 Customer Management
- Customer Registration
- Customer Purchase History
- Loyalty Tracking

### 🧾 Billing System
- Generate Bills
- Automatic Stock Deduction
- Invoice Generation
- Revenue Tracking

### 🚚 Procurement
- Purchase Orders
- Wholesaler Management
- Order Approval
- Automatic Expense Deduction

### 👨‍💼 Staff Management
- Staff Accounts
- Activity Logging
- Role Management

### 📊 Business Analytics
- Revenue Dashboard
- Sales Trend
- Top Selling Products
- Business Value
- Cash Balance
- Profit Analytics

### 🔐 Security
- Login Monitoring
- Security Alerts
- Activity Logs

---

# 🤖 AI Agents

The system includes multiple intelligent agents:

- 📦 Inventory Agent
- 💰 Finance Agent
- 📈 Demand Prediction Agent
- ❤️ Customer Loyalty Agent
- ⚠️ Monitoring Agent
- 🔒 Security Agent
- 📊 Business Analytics Agent

---

# 🛠 Tech Stack

## Backend
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic
- JWT Authentication

## Frontend
- Streamlit
- Plotly
- Pandas

## Database
- MySQL

## AI & Analytics
- Python
- Scikit-Learn
- Pandas
- NumPy

---

# 📂 Project Structure

```
business-automation-ai
│
├── backend
│   ├── app
│   │   ├── models
│   │   ├── routes
│   │   ├── schema
│   │   ├── services
│   │   ├── utils
│   │   └── database.py
│   │
│   ├── requirements.txt
│   └── main.py
│
├── frontend
│   ├── assets
│   ├── components
│   ├── pages
│   ├── utils
│   ├── app.py
│   └── requirements.txt
│
├── screenshots
├── README.md
└── .gitignore
```

---

# 📊 Dashboard

The dashboard provides:

- Total Revenue
- Total Sales
- Business Value
- Inventory Value
- Cash Balance
- Sales Analytics
- Low Stock Alerts
- Top Products
- Activity Timeline

---

# 🔒 Security Features

- JWT Authentication
- Password Hashing
- Activity Logging
- Security Alerts
- Multi-Business Data Isolation

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/Shreyasrinivas121/Business-Automation-using-Multi-Agent-System.git
```

## Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

pip install -r requirements.txt

streamlit run app.py
```

---

# 💻 Technologies Used

- Python
- FastAPI
- Streamlit
- SQLAlchemy
- MySQL
- Plotly
- JWT
- HTML
- CSS

---

# 📸 Screenshots

> Add screenshots here.

Example:

- Login Page
- Dashboard
- Billing
- Inventory
- Analytics
- Procurement
- AI Assistant

---

# 🔮 Future Enhancements

- AI Chat Assistant
- Email Notifications
- WhatsApp Integration
- Mobile Application
- Cloud Deployment (AWS/Azure)
- Predictive Business Analytics

---

# 👨‍💻 Author

**Shreya S**

Artificial Intelligence & Data Science Engineering

Siddaganga Institute of Technology

---

# ⭐ If you found this project useful, consider giving it a star!
