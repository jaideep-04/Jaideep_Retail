from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.database.connection import SessionLocal
from src.database.models import Transaction, Customer, Product
from datetime import datetime, timedelta
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
# ANALYTICS ENDPOINTS
# ============================================================================

@router.get("/overview", tags=["Analytics"])
async def get_analytics_overview(db: Session = Depends(get_db)):
    """Get overall business metrics"""
    try:
        # Total metrics
        total_transactions = db.query(func.count(Transaction.transaction_id)).scalar()
        total_customers = db.query(func.count(Customer.customer_id)).scalar()
        total_products = db.query(func.count(Product.stock_code)).scalar()
        
        # Revenue metrics
        total_revenue = db.query(
            func.sum(Transaction.unit_price * Transaction.quantity)
        ).scalar() or 0
        
        # Transaction status breakdown
        status_summary = db.query(
            Transaction.transaction_status,
            func.count(Transaction.transaction_id).label("count")
        ).group_by(Transaction.transaction_status).all()
        
        return {
            "status": "success",
            "data": {
                "total_transactions": total_transactions,
                "total_customers": total_customers,
                "total_products": total_products,
                "total_revenue": round(float(total_revenue), 2),
                "transaction_status_breakdown": [
                    {"status": s[0], "count": s[1]} for s in status_summary
                ]
            }
        }
    except Exception as e:
        logger.error(f"Error fetching analytics overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monthly-revenue", tags=["Analytics"])
async def get_monthly_revenue(db: Session = Depends(get_db)):
    """Get revenue by month"""
    try:
        monthly_revenue = db.query(
            func.year(Transaction.invoice_date).label("year"),
            func.month(Transaction.invoice_date).label("month"),
            func.sum(Transaction.unit_price * Transaction.quantity).label("revenue"),
            func.count(Transaction.transaction_id).label("transaction_count")
        ).group_by(
            func.year(Transaction.invoice_date),
            func.month(Transaction.invoice_date)
        ).order_by(
            func.year(Transaction.invoice_date),
            func.month(Transaction.invoice_date)
        ).all()
        
        return {
            "status": "success",
            "data": [
                {
                    "year": m[0],
                    "month": m[1],
                    "revenue": round(float(m[2]), 2),
                    "transaction_count": m[3]
                } for m in monthly_revenue
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching monthly revenue: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/country-revenue", tags=["Analytics"])
async def get_revenue_by_country(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get revenue by country"""
    try:
        country_revenue = db.query(
            Customer.country,
            func.sum(Transaction.unit_price * Transaction.quantity).label("total_revenue"),
            func.count(Transaction.transaction_id).label("transaction_count"),
            func.count(func.distinct(Transaction.customer_id)).label("unique_customers")
        ).join(
            Customer, Transaction.customer_id == Customer.customer_id
        ).group_by(
            Customer.country
        ).order_by(
            func.sum(Transaction.unit_price * Transaction.quantity).desc()
        ).limit(limit).all()
        
        return {
            "status": "success",
            "data": [
                {
                    "country": c[0],
                    "total_revenue": round(float(c[1]), 2),
                    "transaction_count": c[2],
                    "unique_customers": c[3]
                } for c in country_revenue
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching country revenue: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/product-category-analysis", tags=["Analytics"])
async def get_product_analysis(db: Session = Depends(get_db)):
    """Analyze product performance"""
    try:
        analysis = db.query(
            Transaction.stock_code,
            Product.description,
            func.sum(Transaction.quantity).label("total_quantity"),
            func.sum(Transaction.unit_price * Transaction.quantity).label("total_revenue"),
            func.count(func.distinct(Transaction.customer_id)).label("unique_customers")
        ).join(
            Product, Transaction.stock_code == Product.stock_code
        ).group_by(
            Transaction.stock_code,
            Product.description
        ).order_by(
            func.sum(Transaction.unit_price * Transaction.quantity).desc()
        ).limit(50).all()
        
        return {
            "status": "success",
            "data": [
                {
                    "stock_code": a[0],
                    "description": a[1],
                    "total_quantity": int(a[2]),
                    "total_revenue": round(float(a[3]), 2),
                    "unique_customers": a[4]
                } for a in analysis
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching product analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customer-segments", tags=["Analytics"])
async def get_customer_segments(db: Session = Depends(get_db)):
    """Segment customers by spending"""
    try:
        customer_spending = db.query(
            Transaction.customer_id,
            Customer.country,
            func.sum(Transaction.unit_price * Transaction.quantity).label("total_spent"),
            func.count(Transaction.transaction_id).label("transaction_count")
        ).join(
            Customer, Transaction.customer_id == Customer.customer_id
        ).filter(
            Transaction.customer_id != '0'
        ).group_by(
            Transaction.customer_id,
            Customer.country
        ).all()
        
        # Segment customers
        segments = {"high_value": 0, "medium_value": 0, "low_value": 0}
        top_10_percent = (len(customer_spending) * 10) // 100 if customer_spending else 0
        
        for idx, customer in enumerate(customer_spending):
            total_spent = float(customer.total_spent or 0)
            
            if idx < top_10_percent:
                segments["high_value"] += 1
            elif idx < top_10_percent * 3:
                segments["medium_value"] += 1
            else:
                segments["low_value"] += 1
        
        return {
            "status": "success",
            "data": segments,
            "total_customers": len(customer_spending)
        }
    except Exception as e:
        logger.error(f"Error fetching customer segments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary", tags=["Analytics"])
async def get_summary_stats(db: Session = Depends(get_db)):
    """Get key summary statistics"""
    try:
        # Calculate various metrics
        total_revenue = db.query(
            func.sum(Transaction.unit_price * Transaction.quantity)
        ).scalar() or 0
        
        avg_transaction_value = db.query(
            func.avg(Transaction.unit_price * Transaction.quantity)
        ).scalar() or 0
        
        total_quantity_sold = db.query(
            func.sum(Transaction.quantity)
        ).scalar() or 0
        
        cancelled_transactions = db.query(
            func.count(Transaction.transaction_id)
        ).filter(
            Transaction.transaction_status == 'CANCELLED'
        ).scalar()
        
        return {
            "status": "success",
            "data": {
                "total_revenue": round(float(total_revenue), 2),
                "avg_transaction_value": round(float(avg_transaction_value), 2),
                "total_quantity_sold": int(total_quantity_sold),
                "cancelled_transactions": cancelled_transactions
            }
        }
    except Exception as e:
        logger.error(f"Error fetching summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))