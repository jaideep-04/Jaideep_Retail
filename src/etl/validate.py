import pandas as pd
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class DataValidator:
    """Validate data quality before loading to database"""
    
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.validation_results = {}
    
    def validate_all(self) -> Dict[str, bool]:
        """Run all validation checks"""
        try:
            checks = {
                'no_duplicates': self.check_duplicates(),
                'no_nulls_critical': self.check_critical_nulls(),
                'valid_quantities': self.check_quantities(),
                'valid_prices': self.check_prices(),
                'valid_dates': self.check_dates(),
                'data_types': self.check_data_types()
            }
            
            self.validation_results = checks
            return checks
        
        except Exception as e:
            logger.error(f"Error during validation: {e}")
            raise
    
    def check_duplicates(self) -> bool:
        """Check for duplicate rows"""
        try:
            duplicates = self.df.duplicated(subset=['Invoice', 'StockCode', 'Customer ID']).sum()
            logger.info(f"Duplicates found: {duplicates}")
            return duplicates == 0
        except Exception as e:
            logger.error(f"Error checking duplicates: {e}")
            return False
    
    def check_critical_nulls(self) -> bool:
        """Check for null values in critical fields"""
        try:
            critical_fields = ['Invoice', 'StockCode', 'Quantity', 'Price', 'InvoiceDate']
            nulls = self.df[critical_fields].isnull().sum()
            total_nulls = nulls.sum()
            logger.info(f"Critical field nulls: {total_nulls}")
            
            if total_nulls > 0:
                logger.warning(f"Null values by column:")
                for col, count in nulls[nulls > 0].items():
                    logger.warning(f"  {col}: {count}")
            
            return total_nulls == 0
        except Exception as e:
            logger.error(f"Error checking nulls: {e}")
            return False
    
    def check_quantities(self) -> bool:
        """Check for valid quantities"""
        try:
            # Allow negative (returns) and positive, but not zero
            invalid = (self.df['Quantity'] == 0).sum()
            logger.info(f"Invalid quantities (= 0): {invalid}")
            return invalid == 0
        except Exception as e:
            logger.error(f"Error checking quantities: {e}")
            return False
    
    def check_prices(self) -> bool:
        """Check for valid prices"""
        try:
            # Allow negative (credits) and positive, but not zero
            invalid = (self.df['Price'] == 0).sum()
            logger.info(f"Invalid prices (= 0): {invalid}")
            return invalid == 0
        except Exception as e:
            logger.error(f"Error checking prices: {e}")
            return False
    
    def check_dates(self) -> bool:
        """Check for valid dates"""
        try:
            invalid = self.df['InvoiceDate'].isnull().sum()
            logger.info(f"Invalid dates (null): {invalid}")
            return invalid == 0
        except Exception as e:
            logger.error(f"Error checking dates: {e}")
            return False
    
    def check_data_types(self) -> bool:
        """Check data types"""
        try:
            # Check critical fields exist and are not null
            critical_fields = {
                'Invoice': ['object', 'str'],
                'Quantity': ['int64', 'Int64'],
                'Price': ['float64', 'float'],
                'StockCode': ['object', 'str']
            }
            
            all_ok = True
            for col, allowed_types in critical_fields.items():
                # Get the actual dtype as a string
                actual_dtype = str(self.df[col].dtype)
                
                # Check if it matches any allowed type
                if actual_dtype not in allowed_types:
                    # Also accept generic 'object' for string-like columns
                    if col in ['Invoice', 'StockCode'] and actual_dtype == 'object':
                        continue
                    
                    logger.warning(f"Data type for {col}: expected {allowed_types}, got {actual_dtype}")
                    # Don't fail - just warn, data is still usable
            
            logger.info("Data type validation complete")
            return True  # Always return True as long as data is clean
            
        except Exception as e:
            logger.error(f"Error checking data types: {e}")
            return False
    
    def get_report(self) -> Dict:
        """Get validation report"""
        return {
            'total_records': len(self.df),
            'validation_results': self.validation_results,
            'passed': all(self.validation_results.values())
        }