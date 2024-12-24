from .supabase_config import get_supabase_client

class SupabaseAdapter:
    def __init__(self):
        self.supabase = get_supabase_client()

    def get_products(self, limit=10, offset=0):
        try:
            response = self.supabase.table('products')\
                .select('*, category:categories(*), brand:brands(*)')\
                .limit(limit)\
                .offset(offset)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Erreur lors de la récupération des produits: {str(e)}")
            return []

    def get_product_by_slug(self, slug):
        try:
            response = self.supabase.table('products')\
                .select('*, category:categories(*), brand:brands(*)')\
                .eq('slug', slug)\
                .single()\
                .execute()
            return response.data
        except Exception as e:
            print(f"Erreur lors de la récupération du produit {slug}: {str(e)}")
            return None

    def get_categories(self):
        try:
            response = self.supabase.table('categories')\
                .select('*')\
                .execute()
            return response.data
        except Exception as e:
            print(f"Erreur lors de la récupération des catégories: {str(e)}")
            return []

    def get_brands(self):
        try:
            response = self.supabase.table('brands')\
                .select('*')\
                .execute()
            return response.data
        except Exception as e:
            print(f"Erreur lors de la récupération des marques: {str(e)}")
            return []

    def get_brand_by_slug(self, slug):
        try:
            response = self.supabase.table('brands')\
                .select('*')\
                .eq('slug', slug)\
                .single()\
                .execute()
            return response.data
        except Exception as e:
            print(f"Erreur lors de la récupération de la marque {slug}: {str(e)}")
            return None

    def create_product(self, product_data):
        try:
            response = self.supabase.table('products')\
                .insert(product_data)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erreur lors de la création du produit: {str(e)}")
            return None

    def update_product(self, product_id, product_data):
        try:
            response = self.supabase.table('products')\
                .update(product_data)\
                .eq('id', product_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erreur lors de la mise à jour du produit: {str(e)}")
            return None

    def delete_product(self, product_id):
        try:
            response = self.supabase.table('products')\
                .delete()\
                .eq('id', product_id)\
                .execute()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression du produit: {str(e)}")
            return False

    def get_reviews_by_product(self, product_id):
        try:
            response = self.supabase.table('reviews')\
                .select('*')\
                .eq('product_id', product_id)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Erreur lors de la récupération des avis: {str(e)}")
            return []

    def create_review(self, review_data):
        try:
            response = self.supabase.table('reviews')\
                .insert(review_data)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erreur lors de la création de l'avis: {str(e)}")
            return None

    def update_review(self, review_id, user_id, review_data):
        try:
            response = self.supabase.table('reviews')\
                .update(review_data)\
                .eq('id', review_id)\
                .eq('user_id', user_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'avis: {str(e)}")
            return None

    def delete_review(self, review_id, user_id):
        try:
            response = self.supabase.table('reviews')\
                .delete()\
                .eq('id', review_id)\
                .eq('user_id', user_id)\
                .execute()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'avis: {str(e)}")
            return False
