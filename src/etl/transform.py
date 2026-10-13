import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataTransformer:
    """Transform and clean data"""
    
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()
        self.transformation_log = []
    
    def clean_data(self) -> pd.DataFrame:
        """Clean and standardize data"""
        try:
            logger.info("Starting data cleaning...")
            
            # Step 1: Remove exact duplicates
            initial_count = len(self.df)
            self.df = self.df.drop_duplicates(
                subset=['Invoice', 'StockCode', 'Customer ID'],
                keep='first'
            )
            duplicates_removed = initial_count - len(self.df)
            self.transformation_log.append(f"Removed {duplicates_removed} duplicate records")
            logger.info(f"Removed {duplicates_removed} duplicates")
            
            # Step 2: Remove rows with missing critical fields
            initial_count = len(self.df)
            self.df = self.df.dropna(
                subset=['Invoice', 'StockCode', 'Quantity', 'Price']
            )
            removed = initial_count - len(self.df)
            self.transformation_log.append(f"Removed {removed} records with missing critical fields")
            logger.info(f"Removed {removed} records with missing critical fields")
            
            # Step 3: Convert data types
            self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'], errors='coerce')
            self.df['Quantity'] = pd.to_numeric(self.df['Quantity'], errors='coerce').astype('Int64')
            self.df['Price'] = pd.to_numeric(self.df['Price'], errors='coerce').astype('float64')
            self.df['Customer ID'] = self.df['Customer ID'].fillna(0).astype('Int64').astype(str)
            self.df['StockCode'] = self.df['StockCode'].astype(str).str.strip().str.upper()
            
            # Remove duplicates again after StockCode standardization
            initial_count = len(self.df)
            self.df = self.df.drop_duplicates(
                subset=['Invoice', 'StockCode', 'Customer ID'],
                keep='first'
            )
            duplicates_removed_after = initial_count - len(self.df)
            if duplicates_removed_after > 0:
                self.transformation_log.append(f"Removed {duplicates_removed_after} additional duplicates after standardization")
                logger.info(f"Removed {duplicates_removed_after} additional duplicates after standardization")
            
            self.transformation_log.append("Converted data types")
            logger.info("Data types converted")
            
            # Step 4: Remove records with invalid quantities/prices
            initial_count = len(self.df)
            # Keep negative quantities (they are returns) but remove zero quantities
            self.df = self.df[self.df['Quantity'] != 0]
            # Remove zero and extremely negative prices (keep legitimate returns/credits)
            self.df = self.df[self.df['Price'] != 0]
            removed = initial_count - len(self.df)
            self.transformation_log.append(f"Removed {removed} records with invalid quantities/prices")
            logger.info(f"Removed {removed} invalid records")
            
            # Step 5: Standardize text fields
            self.df['Description'] = self.df['Description'].fillna('UNKNOWN').str.strip().str.upper()
            self.df['Country'] = self.df['Country'].str.strip().str.upper()
            self.df['Invoice'] = self.df['Invoice'].astype(str).str.strip().str.upper()
            self.transformation_log.append("Standardized text fields")
            logger.info("Text fields standardized")
            
            logger.info(f"Cleaning complete. Records remaining: {len(self.df)}")
            return self.df
        
        except Exception as e:
            logger.error(f"Error during cleaning: {e}")
            raise
    
    def enrich_data(self) -> pd.DataFrame:
        """Add calculated and derived fields"""
        try:
            logger.info("Starting data enrichment...")
            
            # Calculate revenue
            self.df['Revenue'] = (self.df['Quantity'] * self.df['Price']).round(2)
            
            # Extract date components
            self.df['Year'] = self.df['InvoiceDate'].dt.year
            self.df['Month'] = self.df['InvoiceDate'].dt.month
            self.df['Day'] = self.df['InvoiceDate'].dt.day
            self.df['DayOfWeek'] = self.df['InvoiceDate'].dt.day_name()
            self.df['Quarter'] = self.df['InvoiceDate'].dt.quarter
            self.df['WeekOfYear'] = self.df['InvoiceDate'].dt.isocalendar().week
            
            # Add transaction status
            self.df['TransactionStatus'] = 'COMPLETED'
            # Mark cancelled orders
            self.df.loc[self.df['Invoice'].str.startswith('C', na=False), 'TransactionStatus'] = 'CANCELLED'
            
            self.transformation_log.append("Added calculated and derived fields")
            logger.info("Data enrichment complete")
            
            return self.df
        
        except Exception as e:
            logger.error(f"Error during enrichment: {e}")
            raise
    
    def get_log(self):
        """Get transformation log"""
        return self.transformation_log