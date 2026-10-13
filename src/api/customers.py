from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.database.connection import SessionLocal
from src.database.models import Customer, Transaction
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
# CUSTOMER ENDPOINTS
# ============================================================================

@router.get("/")
async def get_all_customers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all customers with pagination"""
    try:
        customers = db.query(Customer)\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        total = db.query(func.count(Customer.customer_id)).scalar()
        
        return {
            "status": "success",
            "data": customers,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "total": total
            }
        }
    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{customer_id}")
async def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """Get specific customer by ID"""
    try:
        customer = db.query(Customer)\
            .filter(Customer.customer_id == customer_id)\
            .first()
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Get customer statistics
        stats = db.query(
            func.count(Transaction.transaction_id).label("total_transactions"),
            func.sum(Transaction.unit_price * Transaction.quantity).label("total_spent"),
            func.avg(Transaction.unit_price * Transaction.quantity).label("avg_order_value")
        ).filter(Transaction.customer_id == customer_id).first()
        
        return {
            "status": "success",
            "data": customer,
            "statistics": {
                "total_transactions": stats.total_transactions or 0,
                "total_spent": round(float(stats.total_spent or 0), 2),
                "avg_order_value": round(float(stats.avg_order_value or 0), 2)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching customer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/country/{country}")
async def get_customers_by_country(
    country: str,
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get customers from specific country"""
    try:
        customers = db.query(Customer)\
            .filter(Customer.country == country.upper())\
            .limit(limit)\
            .all()
        
        if not customers:
            raise HTTPException(status_code=404, detail="No customers found for this country")
        
        return {
            "status": "success",
            "country": country,
            "customer_count": len(customers),
            "data": customers
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching customers by country: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/by-country")
async def get_customers_by_country_stats(db: Session = Depends(get_db)):
    """Get customer count by country"""
    try:
        stats = db.query(
            Customer.country,
            func.count(Customer.customer_id).label("customer_count")
        ).group_by(Customer.country).order_by(
            func.count(Customer.customer_id).desc()
        ).all()
        
        return {
            "status": "success",
            "data": [
                {"country": s[0], "customer_count": s[1]} for s in stats
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching country stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/total-count")
async def get_customer_count(db: Session = Depends(get_db)):
    """Get total customer count"""
    try:
        total = db.query(func.count(Customer.customer_id)).scalar()
        
        return {
            "status": "success",
            "data": {
                "total_customers": total
            }
        }
    except Exception as e:
        logger.error(f"Error fetching customer count: {e}")
        raise HTTPException(status_code=500, detail=str(e))