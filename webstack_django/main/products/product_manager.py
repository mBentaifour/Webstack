from typing import Dict, List, Optional
from ..supabase.client import get_supabase_client
import logging
from slugify import slugify

logger = logging.getLogger(__name__)

class ProductManager:
    """Gestionnaire des produits utilisant Supabase"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def create_product(self, product_data: Dict) -> Dict:
        """Crée un nouveau produit"""
        try:
            # Génération du slug
            if "name" in product_data:
                product_data["slug"] = slugify(product_data["name"])
            
            response = self.supabase.table("products").insert(product_data).execute()
            
            if response.data:
                return {"success": True, "data": response.data[0]}
            return {"success": False, "error": "Échec de la création du produit"}
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du produit : {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_product_by_id(self, product_id: str) -> Dict:
        """Récupère un produit par son ID"""
        try:
            response = self.supabase.table("products") \
                .select("*, category:categories(*), brand:brands(*)") \
                .eq("id", product_id) \
                .single() \
                .execute()
            
            if response.data:
                return {"success": True, "data": response.data}
            return {"success": False, "error": "Produit non trouvé"}
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du produit : {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_products(self, 
                    limit: int = 10,
                    offset: int = 0,
                    category_id: Optional[str] = None,
                    brand_id: Optional[str] = None,
                    min_price: Optional[float] = None,
                    max_price: Optional[float] = None,
                    sort_by: str = "created_at") -> Dict:
        """Récupère une liste de produits avec filtres"""
        try:
            query = self.supabase.table("products") \
                .select("*, category:categories(*), brand:brands(*)") \
                .eq("is_active", True)
            
            # Application des filtres
            if category_id:
                query = query.eq("category_id", category_id)
            if brand_id:
                query = query.eq("brand_id", brand_id)
            if min_price is not None:
                query = query.gte("price", min_price)
            if max_price is not None:
                query = query.lte("price", max_price)
            
            # Tri
            if sort_by == "price_asc":
                query = query.order("price", desc=False)
            elif sort_by == "price_desc":
                query = query.order("price", desc=True)
            else:
                query = query.order("created_at", desc=True)
            
            # Pagination
            query = query.range(offset, offset + limit - 1)
            
            response = query.execute()
            
            if response.data is not None:
                return {"success": True, "data": response.data}
            return {"success": False, "error": "Erreur lors de la récupération des produits"}
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des produits : {str(e)}")
            return {"success": False, "error": str(e)}
    
    def update_product(self, product_id: str, update_data: Dict) -> Dict:
        """Met à jour un produit"""
        try:
            # Mise à jour du slug si le nom change
            if "name" in update_data:
                update_data["slug"] = slugify(update_data["name"])
            
            response = self.supabase.table("products") \
                .update(update_data) \
                .eq("id", product_id) \
                .execute()
            
            if response.data:
                return {"success": True, "data": response.data[0]}
            return {"success": False, "error": "Produit non trouvé"}
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du produit : {str(e)}")
            return {"success": False, "error": str(e)}
    
    def delete_product(self, product_id: str) -> Dict:
        """Suppression douce d'un produit"""
        try:
            response = self.supabase.table("products") \
                .update({"is_active": False}) \
                .eq("id", product_id) \
                .execute()
            
            if response.data:
                return {"success": True, "data": response.data[0]}
            return {"success": False, "error": "Produit non trouvé"}
            
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du produit : {str(e)}")
            return {"success": False, "error": str(e)}
