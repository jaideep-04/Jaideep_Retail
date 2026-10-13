# 🛍️ Retail Transaction Analytics Platform

> **A comprehensive data analytics platform for retail businesses**
> 
> *Built with Python, FastAPI, MySQL, and Streamlit*

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Project Phases](#project-phases)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Dashboard Features](#dashboard-features)
- [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)
- [Team](#team)

---

## 🎯 Overview

The **Retail Transaction Analytics Platform** is a full-stack data analytics application designed to help retail businesses analyze transaction patterns, customer behavior, and product performance. The system processes large volumes of transaction data and provides real-time insights through an interactive dashboard.

**Key Metrics:**
- 🔢 **525,461** transaction records processed
- 📦 **4,632** unique products catalogued
- 👥 **4,383** customer profiles
- 🌍 **40** countries covered
- ⚡ **Real-time** analytics and reporting

---

## ✨ Features

### 📊 Analytics Dashboard
- **Real-time metrics** - KPIs, trends, and key statistics
- **Revenue Analysis** - Monthly trends, country-wise breakdown
- **Product Intelligence** - Top performers, revenue vs. quantity analysis
- **Customer Insights** - Segmentation, top customers, country filtering
- **Advanced Search** - Product lookup and performance analysis
- **Dark Professional Theme** - Grafana-inspired styling for better visibility

### 🔌 REST API
- **Transactions API** - Query, filter, and analyze transaction data
- **Products API** - Product catalog and performance metrics
- **Customers API** - Customer data and segmentation
- **Analytics API** - Aggregated insights and statistics
- **Full Documentation** - Interactive Swagger/OpenAPI docs at `/docs`

### 📈 ETL Pipeline
- **Automated Extraction** - Reads from Excel/CSV data sources
- **Data Transformation** - Cleaning, validation, and standardization
- **Quality Assurance** - Data validation and integrity checks
- **Bulk Loading** - Efficient insertion into MySQL database
- **Error Handling** - Comprehensive logging and error recovery

### 🔐 Database
- **Relational Schema** - Properly normalized tables
- **Data Integrity** - Foreign keys, constraints, and validation
- **Scalable Design** - Optimized for large datasets
- **Referential Integrity** - Maintained across all tables

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | FastAPI | 0.104.1+ |
| **Frontend** | Streamlit | 1.28.1+ |
| **Database** | MySQL | 8.0+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Data Processing** | Pandas | 2.0+ |
| **Server** | Uvicorn | 0.24.0+ |
| **Language** | Python | 3.12.0 |
| **Testing** | Pytest | 9.1.1+ |

---

## 📁 Project Structure

```
retail-analytics-platform/
├── src/
│   ├── api/                          # FastAPI application
│   │   ├── __init__.py
│   │   ├── main.py                   # API entry point
│   │   ├── transactions.py           # Transaction endpoints
│   │   ├── products.py               # Product endpoints
│   │   ├── customers.py              # Customer endpoints
│   │   └── analytics.py              # Analytics endpoints
│   │
│   ├── database/                     # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py             # Database connection setup
│   │   ├── models.py                 # SQLAlchemy models
│   │   └── schema.sql                # SQL schema definition
│   │
│   ├── etl/                          # ETL pipeline
│   │   ├── __init__.py
│   │   ├── extract.py                # Data extraction
│   │   ├── transform.py              # Data transformation
│   │   ├── validate.py               # Data validation
│   │   ├── load.py                   # Data loading
│   │   └── etl_pipeline.py           # Main pipeline orchestrator
│   │
│   ├── dashboard/                    # Streamlit dashboard
│   │   ├── __init__.py
│   │   └── dashboard.py              # Main dashboard app
│   │
│   └── eda/                          # Exploratory Data Analysis
│       ├── exploratory_analysis.py
│       ├── data_quality_check.py
│       └── __init__.py
│
├── data/
│   └── sample_data/
│       └── online_retail.xlsx        # Source dataset
│
├── docs/
│   ├── API_DOCS.md                   # API reference
│   ├── ARCHITECTURE.md               # System design
│   └── Dataset_Details.md            # Data documentation
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # Pytest fixtures
│   ├── test_api.py                   # API tests
│   ├── test_etl.py                   # ETL pipeline tests
│   └── test_database.py              # Database tests
│
├── .env                              # Environment variables (local)
├── .gitignore                        # Git ignore rules
├── requirements.txt                  # Python dependencies
├── pytest.ini                        # Pytest configuration
└── README.md                         # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.12+** - [Download](https://www.python.org/downloads/)
- **MySQL 8.0+** - [Download](https://dev.mysql.com/downloads/mysql/)
- **Git** - [Download](https://git-scm.com/)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/retail-analytics-platform.git
cd retail-analytics-platform
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=retail_user
DB_PASSWORD=your_secure_password
DB_NAME=retail_analytics

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Dashboard Configuration
STREAMLIT_PORT=8501
```

### Step 5: Setup MySQL Database

```bash
# Log into MySQL
mysql -u root -p

# Create database and user
CREATE DATABASE retail_analytics;
CREATE USER 'retail_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON retail_analytics.* TO 'retail_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 6: Run ETL Pipeline

```bash
python -m src.etl.etl_pipeline
```

**Expected Output:**
```
Extracting data...
Transforming data...
Validating data...
Loading data...
✅ ETL Pipeline Complete!
- Products loaded: 4,116
- Transactions loaded: 508,456
```

---

## 🎮 Running the Application

### Terminal 1: Start the API

```bash
uvicorn src.api.main:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Access:**
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Terminal 2: Start the Dashboard

```bash
streamlit run src/dashboard/dashboard.py
```

**Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Access Dashboard

Open your browser and navigate to: **http://localhost:8501**

---

## 📊 Project Phases

### ✅ Phase 1: Setup
- Environment configuration
- Folder structure
- Dependencies management

### ✅ Phase 2: Exploratory Data Analysis (EDA)
- Dataset investigation
- Data quality checks
- Statistical analysis

### ✅ Phase 3: Database Setup
- MySQL configuration
- User creation
- Schema design

### ✅ Phase 4: ETL Pipeline
- Data extraction from Excel
- Transformation and cleaning
- Data validation
- Loading into MySQL

### ✅ Phase 5: REST API
- FastAPI application setup
- CRUD operations
- Analytics endpoints
- Error handling

### ✅ Phase 6: Streamlit Dashboard
- Interactive visualizations
- Multiple analytics pages
- Real-time data display
- Professional styling

### ✅ Phase 7: Testing
- API endpoint tests
- ETL pipeline tests
- Database model tests
- Data integrity tests

### ⏳ Phase 8: Documentation
- API reference
- Architecture guide
- Setup instructions

### ⏳ Phase 9: Presentation
- Project overview
- Results and insights
- Demo walkthrough

### ⏳ Phase 10: GitHub Submission
- Repository finalization
- Final submission

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
# API tests
pytest tests/test_api.py -v

# ETL tests
pytest tests/test_etl.py -v

# Database tests
pytest tests/test_database.py -v
```

### Generate Coverage Report

```bash
pytest tests/ --cov=src --cov-report=html
```

### Test Results

```
======================== 21 passed in 2.74s =========================
✅ All tests passing
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Transactions Endpoints

#### Get All Transactions
```
GET /transactions/
```

**Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Number of records to return (default: 10)
- `country` (str): Filter by country

**Response:**
```json
{
  "total": 508456,
  "data": [
    {
      "invoice": "536365",
      "stock_code": "85123A",
      "quantity": 6,
      "price": 2.55,
      "customer_id": "12345",
      "country": "UNITED KINGDOM"
    }
  ]
}
```

#### Get Transaction Statistics
```
GET /transactions/stats
```

**Response:**
```json
{
  "total_transactions": 508456,
  "total_revenue": 9000000.00,
  "avg_transaction_value": 17.72,
  "unique_customers": 4383,
  "unique_products": 4116
}
```

### Products Endpoints

#### Get All Products
```
GET /products/
```

**Response:**
```json
{
  "total": 4116,
  "data": [
    {
      "stock_code": "85123A",
      "description": "White Hanging Heart T-Light Holder",
      "current_price": 2.55
    }
  ]
}
```

#### Get Top Products
```
GET /products/top?limit=10
```

**Response:**
```json
[
  {
    "stock_code": "85123A",
    "description": "Product Name",
    "total_sold": 1000,
    "total_revenue": 2550.00
  }
]
```

### Customers Endpoints

#### Get All Customers
```
GET /customers/
```

#### Get Customer Segments
```
GET /analytics/customer-segments
```

**Response:**
```json
{
  "high_value": 438,
  "medium_value": 876,
  "low_value": 3067
}
```

### Analytics Endpoints

#### Get Overview Statistics
```
GET /analytics/overview
```

**Response:**
```json
{
  "total_revenue": 9000000.00,
  "total_transactions": 508456,
  "avg_order_value": 17.72,
  "unique_customers": 4383
}
```

#### Get Daily Revenue
```
GET /analytics/daily-revenue
```

#### Get Top Countries
```
GET /analytics/countries?limit=10
```

---

## 📈 Dashboard Features

### 🏠 Overview Page
- **KPI Cards** - Total Revenue, Transactions, Customers, Products
- **Top Products Chart** - Best-selling products by revenue
- **Top Products Table** - Detailed product metrics
- **Top Customers Table** - Premium customers list

### 💰 Revenue Page
- **Monthly Revenue Trend** - Line chart showing revenue over time
- **Revenue by Country** - Horizontal bar chart
- **Date range filter** - Custom date selection

### 📦 Products Page
- **Revenue Comparison** - Bar chart of product revenues
- **Quantity vs Revenue** - Scatter plot analysis
- **Top/Bottom performers** - Rankings and metrics

### 👥 Customers Page
- **Top Customers Chart** - Revenue contribution
- **Customer Rankings Table** - Detailed metrics
- **Country Filter** - Dynamic filtering

### 🔍 Search Page
- **Product Keyword Search** - Find products by name
- **Detailed Analytics** - Performance metrics for selected product

---

## 🗄️ Database Schema

### Customers Table
```sql
CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    country VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Products Table
```sql
CREATE TABLE products (
    stock_code VARCHAR(20) PRIMARY KEY,
    description VARCHAR(255),
    current_price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    invoice VARCHAR(20) NOT NULL,
    stock_code VARCHAR(20) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    invoice_date DATETIME,
    customer_id VARCHAR(10),
    FOREIGN KEY (stock_code) REFERENCES products(stock_code),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

---

## ❓ Troubleshooting

### MySQL Connection Error
```
Error: Access denied for user 'retail_user'@'localhost'
```
**Solution:**
- Verify MySQL is running: `mysql -u root -p`
- Check `.env` credentials
- Reset user password: `ALTER USER 'retail_user'@'localhost' IDENTIFIED BY 'new_password';`

### ETL Pipeline Fails
```
FileNotFoundError: data/sample_data/online_retail.xlsx
```
**Solution:**
- Ensure data file exists at correct path
- Download from UCI Machine Learning Repository
- Check file permissions

### API Port Already in Use
```
Address already in use: ('127.0.0.1', 8000)
```
**Solution:**
- Kill process: `lsof -ti:8000 | xargs kill -9`
- Or use different port: `uvicorn src.api.main:app --port 8001`

### Dashboard Not Loading
```
StreamlitAPIException: "Page 'Dashboard' not found"
```
**Solution:**
- Ensure API is running on port 8000
- Check network connectivity
- Restart Streamlit: `streamlit run src/dashboard/dashboard.py`

---

## 📦 Dependencies

### Core Dependencies
```
fastapi==0.104.1
uvicorn==0.24.0
streamlit==1.28.1
sqlalchemy==2.0.23
pandas==2.1.1
numpy==1.26.1
pymysql==1.1.0
python-dotenv==1.0.0
```

### Development Dependencies
```
pytest==9.1.1
pytest-cov==7.1.0
```

---

## 👨‍💻 Team

**Student:** Jaideep D.  
**GitHub:** [@jaideep.d](https://github.com)  
**Email:** jaideep.d@example.com

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Dataset:** UCI Machine Learning Repository - Online Retail II Dataset
- **Framework:** FastAPI, Streamlit, SQLAlchemy Communities
- **Database:** MySQL Documentation

---

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the API documentation
3. Check test files for examples
4. Submit an issue on GitHub

---

**Last Updated:** October 13, 2026  
**Status:** ✅ Production Ready

---

*Happy Analyzing! 📊*