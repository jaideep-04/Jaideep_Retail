from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from src.database.connection import SessionLocal
from src.database.models import Transaction
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# TRANSACTION ENDPOINTS
# ============================================================================

@router.get("/", tags=["Transactions"])
async def get_all_transactions(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all transactions with pagination"""
    try:
        transactions = db.query(Transaction)\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        total = db.query(func.count(Transaction.transaction_id)).scalar()
        
        return {
            "status": "success",
            "data": transactions,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "total": total
            }
        }
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{transaction_id}", tags=["Transactions"])
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get specific transaction by ID"""
    try:
        transaction = db.query(Transaction)\
            .filter(Transaction.transaction_id == transaction_id)\
            .first()
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return {
            "status": "success",
            "data": transaction
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/invoice/{invoice_no}", tags=["Transactions"])
async def get_transactions_by_invoice(
    invoice_no: str,
    db: Session = Depends(get_db)
):
    """Get all transactions for a specific invoice"""
    try:
        transactions = db.query(Transaction)\
            .filter(Transaction.invoice_no == invoice_no.upper())\
            .all()
        
        if not transactions:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        total_revenue = sum(t.unit_price * t.quantity for t in transactions)
        
        return {
            "status": "success",
            "invoice_no": invoice_no,
            "transaction_count": len(transactions),
            "total_revenue": round(total_revenue, 2),
            "data": transactions
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching invoice: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customer/{customer_id}", tags=["Transactions"])
async def get_customer_transactions(
    customer_id: str,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all transactions for a specific customer"""
    try:
        transactions = db.query(Transaction)\
            .filter(Transaction.customer_id == customer_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        if not transactions:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        total_spent = sum(t.unit_price * t.quantity for t in transactions)
        
        return {
            "status": "success",
            "customer_id": customer_id,
            "transaction_count": len(transactions),
            "total_spent": round(total_spent, 2),
            "data": transactions
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching customer transactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/summary", tags=["Transactions"])
async def get_transaction_summary(db: Session = Depends(get_db)):
    """Get summary of transaction statuses"""
    try:
        summary = db.query(
            Transaction.transaction_status,
            func.count(Transaction.transaction_id).label("count")
        ).group_by(Transaction.transaction_status).all()
        
        return {
            "status": "success",
            "data": [
                {"status": s[0], "count": s[1]} for s in summary
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/top-customers", tags=["Transactions"])
async def get_top_customers(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get top customers by total spending"""
    try:
        top_customers = db.query(
            Transaction.customer_id,
            func.sum(Transaction.unit_price * Transaction.quantity).label("total_spent"),
            func.count(Transaction.transaction_id).label("transaction_count")
        ).filter(
            Transaction.customer_id != '0'
        ).group_by(
            Transaction.customer_id
        ).order_by(
            desc(func.sum(Transaction.unit_price * Transaction.quantity))
        ).limit(limit).all()
        
        return {
            "status": "success",
            "data": [
                {
                    "customer_id": c[0],
                    "total_spent": round(c[1], 2),
                    "transaction_count": c[2]
                } for c in top_customers
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching top customers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/top-products", tags=["Transactions"])
async def get_top_products(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get top products by quantity sold"""
    try:
        top_products = db.query(
            Transaction.stock_code,
            func.sum(Transaction.quantity).label("total_quantity"),
            func.sum(Transaction.unit_price * Transaction.quantity).label("total_revenue")
        ).filter(
            Transaction.quantity > 0
        ).group_by(
            Transaction.stock_code
        ).order_by(
            desc(func.sum(Transaction.quantity))
        ).limit(limit).all()
        
        return {
            "status": "success",
            "data": [
                {
                    "stock_code": p[0],
                    "total_quantity": int(p[1]),
                    "total_revenue": round(p[2], 2)
                } for p in top_products
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching top products: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/daily-revenue", tags=["Transactions"])
async def get_daily_revenue(db: Session = Depends(get_db)):
    """Get daily revenue"""
    try:
        daily_revenue = db.query(
            func.date(Transaction.invoice_date).label("date"),
            func.sum(Transaction.unit_price * Transaction.quantity).label("total_revenue"),
            func.count(Transaction.transaction_id).label("transaction_count")
        ).group_by(
            func.date(Transaction.invoice_date)
        ).order_by(
            func.date(Transaction.invoice_date)
        ).limit(30).all()
        
        return {
            "status": "success",
            "data": [
                {
                    "date": str(d[0]),
                    "total_revenue": round(d[1], 2),
                    "transaction_count": d[2]
                } for d in daily_revenue
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching daily revenue: {e}")
        raise HTTPException(status_code=500, detail=str(e))