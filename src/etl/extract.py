import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DataExtractor:
    """Extract data from CSV or Excel files"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
    
    def extract(self) -> pd.DataFrame:
        """Extract data from file (CSV or Excel)"""
        try:
            logger.info(f"Starting extraction from: {self.file_path}")
            
            # Check if file exists
            if not Path(self.file_path).exists():
                raise FileNotFoundError(f"File not found: {self.file_path}")
            
            # Read based on file type
            if self.file_path.endswith('.csv'):
                self.data = pd.read_csv(self.file_path)
                logger.info(f"Successfully read CSV file: {self.file_path}")
            
            elif self.file_path.endswith(('.xlsx', '.xls')):
                self.data = pd.read_excel(self.file_path)
                logger.info(f"Successfully read Excel file: {self.file_path}")
            
            else:
                raise ValueError(f"Unsupported file format: {self.file_path}")
            
            # Log summary
            rows, cols = self.data.shape
            logger.info(f"Extracted {rows} rows and {cols} columns")
            
            return self.data
        
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            raise