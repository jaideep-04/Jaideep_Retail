import pytest
import pandas as pd
from datetime import datetime

@pytest.fixture
def sample_customer():
    """Sample customer data"""
    return {
        "customer_id": "12345",
        "country": "UNITED KINGDOM"
    }

@pytest.fixture
def sample_product():
    """Sample product data"""
    return {
        "stock_code": "85123A",
        "description": "White Hanging Heart T-Light Holder",
        "current_price": 2.55
    }

@pytest.fixture
def sample_transaction():
    """Sample transaction data"""
    return {
        "invoice": "536365",
        "stock_code": "85123A",
        "description": "White Hanging Heart T-Light Holder",
        "quantity": 6,
        "invoice_date": datetime(2010, 12, 1, 8, 26, 0),
        "price": 2.55,
        "customer_id": "12345",
        "country": "UNITED KINGDOM",
        "total_amount": 15.30
    }

@pytest.fixture
def sample_dataframe():
    """Sample pandas DataFrame for ETL testing"""
    data = {
        'Invoice': ['536365', '536365', '536366'],
        'StockCode': ['85123A', '71053', '84406B'],
        'Description': ['White Hanging', 'White Metal', 'Cream Cupid'],
        'Quantity': [6, 6, 8],
        'InvoiceDate': [datetime(2010, 12, 1), datetime(2010, 12, 1), datetime(2010, 12, 1)],
        'Price': [2.55, 3.39, 2.75],
        'Customer ID': ['12345', '12345', '12346'],
        'Country': ['UNITED KINGDOM', 'UNITED KINGDOM', 'UNITED KINGDOM']
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_invalid_dataframe():
    """Sample DataFrame with invalid data"""
    data = {
        'Invoice': ['536365', '536365', '536366'],
        'StockCode': ['85123A', '71053', '84406B'],
        'Description': ['White Hanging', 'White Metal', 'Cream Cupid'],
        'Quantity': [6, 0, -5],
        'InvoiceDate': [datetime(2010, 12, 1), datetime(2010, 12, 1), datetime(2010, 12, 1)],
        'Price': [2.55, 0, -1.5],
        'Customer ID': ['12345', '12345', None],
        'Country': ['UNITED KINGDOM', 'UNITED KINGDOM', 'UNITED KINGDOM']
    }
    return pd.DataFrame(data)