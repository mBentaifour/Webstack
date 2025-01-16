from celery import shared_task
from .supabase_adapter import SupabaseAdapter
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_stock_levels():
    """Tâche périodique pour vérifier les niveaux de stock."""
    try:
        db = SupabaseAdapter()
        result = db.check_stock_levels()
        
        if result['success']:
            alerts_count = result['data']['alerts_created']
            logger.info(f"Vérification des stocks terminée : {alerts_count} alertes créées")
        else:
            logger.error("Erreur lors de la vérification des stocks")
            
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la vérification des stocks : {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
