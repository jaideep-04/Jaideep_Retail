import logging
import sys
from src.etl.extract import DataExtractor
from src.etl.transform import DataTransformer
from src.etl.validate import DataValidator
from src.etl.load import DataLoader

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ETLPipeline:
    """Main ETL Pipeline Orchestrator"""
    
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.data = None
    
    def run(self) -> bool:
        """Execute complete ETL pipeline"""
        try:
            logger.info("=" * 80)
            logger.info("STARTING ETL PIPELINE")
            logger.info("=" * 80)
            
            # EXTRACT
            logger.info("\n[1/5] EXTRACT PHASE")
            logger.info("-" * 80)
            extractor = DataExtractor(self.input_file)
            self.data = extractor.extract()
            logger.info(f"✓ Extracted {len(self.data)} records")
            
            # TRANSFORM
            logger.info("\n[2/5] TRANSFORM PHASE")
            logger.info("-" * 80)
            transformer = DataTransformer(self.data)
            self.data = transformer.clean_data()
            logger.info(f"✓ Cleaned data: {len(self.data)} records remaining")
            
            self.data = transformer.enrich_data()
            logger.info(f"✓ Enriched data with calculated fields")
            
            # VALIDATE
            logger.info("\n[3/5] VALIDATE PHASE")
            logger.info("-" * 80)
            validator = DataValidator(self.data)
            validation_results = validator.validate_all()
            validation_report = validator.get_report()
            
            logger.info(f"✓ Validation Results:")
            for check, passed in validation_results.items():
                status = "✓ PASS" if passed else "✗ FAIL"
                logger.info(f"  {status}: {check}")
            
            if not validation_report['passed']:
                logger.error("✗ Validation FAILED! Check logs above.")
                return False
            
            logger.info(f"✓ All validations passed!")
            logger.info(f"✓ Total records to load: {validation_report['total_records']}")
            
            # LOAD
            logger.info("\n[4/5] LOAD PHASE")
            logger.info("-" * 80)
            loader = DataLoader()
            loader.load_to_database(self.data)
            
            # SUCCESS
            logger.info("\n[5/5] SUMMARY")
            logger.info("=" * 80)
            logger.info("✅ ETL PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info("=" * 80)
            logger.info(f"Total records processed: {len(self.data)}")
            logger.info("Next steps:")
            logger.info("  1. Start API: uvicorn src.api.main:app --reload")
            logger.info("  2. Start Dashboard: streamlit run src/dashboard/dashboard.py")
            
            return True
        
        except Exception as e:
            logger.error("=" * 80)
            logger.error("❌ ETL PIPELINE FAILED")
            logger.error("=" * 80)
            logger.error(f"Error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

# Main execution
if __name__ == "__main__":
    input_file = 'data/sample_data/online_retail.xlsx'
    
    pipeline = ETLPipeline(input_file)
    success = pipeline.run()
    
    sys.exit(0 if success else 1)