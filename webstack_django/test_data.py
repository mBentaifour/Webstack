from main.supabase_adapter import SupabaseAdapter
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_data():
    try:
        adapter = SupabaseAdapter()
        
        # Test categories
        categories = adapter.get_categories()
        logger.info(f"Categories found: {categories}")
        
        # Test products
        products = adapter.get_products()
        logger.info(f"Products found: {products}")
        
    except Exception as e:
        logger.error(f"Error testing data: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    test_data()
