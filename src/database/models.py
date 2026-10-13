from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.types import Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# ============================================================================
# CUSTOMERS TABLE MODEL
# ============================================================================
class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(String(10), primary_key=True)
    country = Column(String(50), nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    total_purchases = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Customer(id={self.customer_id}, country={self.country})>"

# ============================================================================
# PRODUCTS TABLE MODEL
# ============================================================================
class Product(Base):
    __tablename__ = "products"
    
    stock_code = Column(String(20), primary_key=True)
    description = Column(String(255), nullable=False)
    category = Column(String(100))
    current_price = Column(Numeric(10, 2))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Product(code={self.stock_code}, desc={self.description})>"

# ============================================================================
# TRANSACTIONS TABLE MODEL
# ============================================================================
class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_no = Column(String(20), nullable=False, index=True)
    customer_id = Column(String(10), ForeignKey("customers.customer_id"))
    stock_code = Column(String(20), ForeignKey("products.stock_code"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    invoice_date = Column(DateTime, nullable=False, index=True)
    transaction_status = Column(String(20), default="COMPLETED")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<Transaction(id={self.transaction_id}, invoice={self.invoice_no})>"