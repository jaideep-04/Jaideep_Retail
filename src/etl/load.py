import pandas as pd
import logging
from sqlalchemy.orm import Session
from src.database.models import Customer, Product, Transaction
from src.database.connection import SessionLocal
from datetime import datetime

logger = logging.getLogger(__name__)

class DataLoader:
    """Load cleaned data into MySQL database"""
    
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
        self.load_log = []
        self.stats = {
            'customers_loaded': 0,
            'products_loaded': 0,
            'transactions_loaded': 0,
            'errors': 0
        }
    
    def load_to_database(self, dataframe: pd.DataFrame) -> bool:
        """Load cleaned data to MySQL database"""
        try:
            logger.info("=" * 80)
            logger.info("STARTING DATA LOAD TO MYSQL")
            logger.info("=" * 80)
            
            # Load customers
            logger.info("\n[1/3] Loading customers...")
            self.load_customers(dataframe)
            
            # Load products
            logger.info("\n[2/3] Loading products...")
            self.load_products(dataframe)
            
            # Load transactions
            logger.info("\n[3/3] Loading transactions...")
            self.load_transactions(dataframe)
            
            # Commit all changes
            self.db.commit()
            
            logger.info("\n" + "=" * 80)
            logger.info("✅ ALL DATA LOADED SUCCESSFULLY!")
            logger.info("=" * 80)
            logger.info(f"Customers loaded: {self.stats['customers_loaded']}")
            logger.info(f"Products loaded: {self.stats['products_loaded']}")
            logger.info(f"Transactions loaded: {self.stats['transactions_loaded']}")
            
            return True
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ ERROR during loading: {e}")
            self.stats['errors'] += 1
            raise
        finally:
            self.db.close()
    
    def load_customers(self, df: pd.DataFrame):
        """Load unique customers"""
        try:
            # Get unique customers
            customers_data = df[['Customer ID', 'Country']].drop_duplicates(subset=['Customer ID'])
            customers_data = customers_data.dropna(subset=['Customer ID'])
            
            count = 0
            for _, row in customers_data.iterrows():
                try:
                    customer_id = str(int(row['Customer ID'])) if row['Customer ID'] != '0' else None
                    
                    if not customer_id or customer_id == 'nan':
                        continue
                    
                    # Check if exists
                    existing = self.db.query(Customer).filter(
                        Customer.customer_id == customer_id
                    ).first()
                    
                    if not existing:
                        customer = Customer(
                            customer_id=customer_id,
                            country=row['Country'],
                            registration_date=datetime.utcnow()
                        )
                        self.db.add(customer)
                        count += 1
                except Exception as e:
                    logger.warning(f"Error loading customer {row['Customer ID']}: {e}")
                    continue
            
            self.db.commit()
            self.stats['customers_loaded'] = count
            logger.info(f"✓ Loaded {count} customers")
            
        except Exception as e:
            logger.error(f"Error loading customers: {e}")
            raise
    
    def load_products(self, df: pd.DataFrame):
        """Load unique products"""
        try:
            # Get unique products
            products_data = df[['StockCode', 'Description', 'Price']].drop_duplicates(subset=['StockCode'])
            
            count = 0
            for _, row in products_data.iterrows():
                try:
                    # Check if exists
                    existing = self.db.query(Product).filter(
                        Product.stock_code == row['StockCode']
                    ).first()
                    
                    if not existing:
                        product = Product(
                            stock_code=row['StockCode'],
                            description=row['Description'],
                            current_price=float(row['Price']) if row['Price'] != 0 else None
                        )
                        self.db.add(product)
                        count += 1
                except Exception as e:
                    logger.warning(f"Error loading product {row['StockCode']}: {e}")
                    continue
            
            self.db.commit()
            self.stats['products_loaded'] = count
            logger.info(f"✓ Loaded {count} products")
            
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            raise
    
    def load_transactions(self, df: pd.DataFrame):
        """Load transaction records"""
        try:
            count = 0
            errors = 0
            
            for idx, row in df.iterrows():
                try:
                    # Get or convert customer ID
                    customer_id = None
                    if pd.notna(row['Customer ID']) and row['Customer ID'] != '0':
                        customer_id = str(int(row['Customer ID']))
                    
                    # Create transaction
                    transaction = Transaction(
                        invoice_no=str(row['Invoice']),
                        customer_id=customer_id,
                        stock_code=str(row['StockCode']),
                        quantity=int(row['Quantity']),
                        unit_price=float(row['Price']),
                        invoice_date=row['InvoiceDate'],
                        transaction_status=row.get('TransactionStatus', 'COMPLETED')
                    )
                    self.db.add(transaction)
                    count += 1
                    
                    # Commit every 1000 records for performance
                    if count % 1000 == 0:
                        self.db.commit()
                        if count % 10000 == 0:
                            logger.info(f"  ✓ Loaded {count} transactions...")
                
                except Exception as e:
                    errors += 1
                    if errors <= 5:  # Log first 5 errors
                        logger.warning(f"Error loading transaction {idx}: {e}")
                    continue
            
            # Final commit
            self.db.commit()
            self.stats['transactions_loaded'] = count
            logger.info(f"✓ Loaded {count} transactions (with {errors} errors)")
            
        except Exception as e:
            logger.error(f"Error loading transactions: {e}")
            raise