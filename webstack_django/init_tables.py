from main.supabase_adapter import SupabaseAdapter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_tables():
    try:
        adapter = SupabaseAdapter()
        adapter.init_tables()
        logger.info("Tables initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing tables: {str(e)}")

if __name__ == "__main__":
    init_tables()