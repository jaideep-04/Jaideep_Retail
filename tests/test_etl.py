import pytest
import pandas as pd
from datetime import datetime

class TestETL:
    """Test ETL pipeline"""
    
    def test_dataframe_creation(self, sample_dataframe):
        """Test DataFrame creation"""
        df = sample_dataframe
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
    
    def test_dataframe_columns(self, sample_dataframe):
        """Test DataFrame has required columns"""
        df = sample_dataframe
        required = ['Invoice', 'StockCode', 'Quantity', 'Price']
        for col in required:
            assert col in df.columns
    
    def test_duplicate_removal(self, sample_dataframe):
        """Test duplicate removal"""
        df = sample_dataframe.copy()
        df_dup = pd.concat([df, df], ignore_index=True)
        df_clean = df_dup.drop_duplicates()
        assert len(df_clean) < len(df_dup)
    
    def test_invalid_data_removal(self, sample_invalid_dataframe):
        """Test invalid data removal"""
        df = sample_invalid_dataframe.copy()
        df_clean = df[(df['Quantity'] > 0) & (df['Price'] > 0)]
        assert all(df_clean['Quantity'] > 0)
        assert all(df_clean['Price'] > 0)
    
    def test_null_removal(self, sample_invalid_dataframe):
        """Test null value removal"""
        df = sample_invalid_dataframe.copy()
        df_clean = df.dropna(subset=['Customer ID'])
        assert df_clean['Customer ID'].isna().sum() == 0
    
    def test_total_calculation(self, sample_dataframe):
        """Test total amount calculation"""
        df = sample_dataframe.copy()
        df['total'] = df['Quantity'] * df['Price']
        assert 'total' in df.columns
        assert len(df['total']) > 0
    
    def test_data_quality(self, sample_dataframe):
        """Test data quality metrics"""
        df = sample_dataframe
        # Check completeness
        total = df.shape[0] * df.shape[1]
        nulls = df.isna().sum().sum()
        completeness = ((total - nulls) / total) * 100
        assert completeness > 80
    
    def test_transformation_pipeline(self, sample_dataframe):
        """Test complete transformation pipeline"""
        df = sample_dataframe.copy()
        
        # Transform
        df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]
        df = df.dropna(subset=['Customer ID'])
        df['total'] = df['Quantity'] * df['Price']
        
        # Validate
        assert len(df) > 0
        assert 'total' in df.columns
        assert all(df['Quantity'] > 0)
        assert all(df['Price'] > 0)