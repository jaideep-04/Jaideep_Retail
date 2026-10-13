from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.database.connection import SessionLocal
from src.database.models import Product, Transaction
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
# PRODUCT ENDPOINTS
# ============================================================================

@router.get("/", tags=["Products"])
async def get_all_products(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active: bool = None
):
    """Get all products with pagination"""
    try:
        query = db.query(Product)
        
        if active is not None:
            query = query.filter(Product.active == active)
        
        products = query.offset(skip).limit(limit).all()
        total = query.count()
        
        return {
            "status": "success",
            "data": products,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "total": total
            }
        }
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{stock_code}", tags=["Products"])
async def get_product(stock_code: str, db: Session = Depends(get_db)):
    """Get specific product by stock code"""
    try:
        product = db.query(Product)\
            .filter(Product.stock_code == stock_code.upper())\
            .first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get sales statistics
        stats = db.query(
            func.count(Transaction.transaction_id).label("times_sold"),
            func.sum(Transaction.quantity).label("total_quantity"),
            func.sum(Transaction.unit_price * Transaction.quantity).label("total_revenue")
        ).filter(Transaction.stock_code == stock_code.upper()).first()
        
        return {
            "status": "success",
            "data": product,
            "statistics": {
                "times_sold": stats.times_sold or 0,
                "total_quantity": int(stats.total_quantity or 0),
                "total_revenue": round(float(stats.total_revenue or 0), 2)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/{query}", tags=["Products"])
async def search_products(
    query: str,
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500)
):
    """Search products by description"""
    try:
        search_term = f"%{query.upper()}%"
        products = db.query(Product)\
            .filter(Product.description.like(search_term))\
            .limit(limit)\
            .all()
        
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        
        return {
            "status": "success",
            "query": query,
            "results_count": len(products),
            "data": products
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/price/range", tags=["Products"])
async def get_products_by_price_range(
    min_price: float = Query(0, ge=0),
    max_price: float = Query(1000, ge=0),
    db: Session = Depends(get_db)
):
    """Get products within price range"""
    try:
        products = db.query(Product)\
            .filter(
                Product.current_price >= min_price,
                Product.current_price <= max_price
            ).all()
        
        return {
            "status": "success",
            "filter": {
                "min_price": min_price,
                "max_price": max_price
            },
            "count": len(products),
            "data": products
        }
    except Exception as e:
        logger.error(f"Error fetching products by price: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/total-count", tags=["Products"])
async def get_product_count(db: Session = Depends(get_db)):
    """Get total product count"""
    try:
        total = db.query(func.count(Product.stock_code)).scalar()
        active = db.query(func.count(Product.stock_code))\
            .filter(Product.active == True).scalar()
        
        return {
            "status": "success",
            "data": {
                "total_products": total,
                "active_products": active,
                "inactive_products": total - active
            }
        }
    except Exception as e:
        logger.error(f"Error fetching product count: {e}")
        raise HTTPException(status_code=500, detail=str(e))