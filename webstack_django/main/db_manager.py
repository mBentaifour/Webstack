from django.conf import settings
from supabase import create_client
from functools import lru_cache

class SupabaseManager:
    def __init__(self):
        self.supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY
        )
        
    @lru_cache(maxsize=None)
    def get_client(self):
        """Retourne une instance du client Supabase."""
        return self.supabase
    
    def get_products(self, limit=None, category=None):
        """Récupère les produits avec filtres optionnels."""
        query = self.supabase.table('products').select('*')
        
        if category:
            query = query.eq('category', category)
        if limit:
            query = query.limit(limit)
            
        return query.execute()
    
    def get_product(self, product_id):
        """Récupère un produit par son ID."""
        return self.supabase.table('products').select('*').eq('id', product_id).single().execute()
    
    def create_product(self, product_data):
        """Crée un nouveau produit."""
        return self.supabase.table('products').insert(product_data).execute()
    
    def update_product(self, product_id, product_data):
        """Met à jour un produit existant."""
        return self.supabase.table('products').update(product_data).eq('id', product_id).execute()
    
    def delete_product(self, product_id):
        """Supprime un produit."""
        return self.supabase.table('products').delete().eq('id', product_id).execute()

# Instance globale du gestionnaire
db = SupabaseManager()
