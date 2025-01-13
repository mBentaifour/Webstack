from .supabase_config import get_supabase_client
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from slugify import slugify
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from functools import lru_cache

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseAdapter:
    """Adaptateur pour interagir avec Supabase"""
    
    def __init__(self):
        """Initialise la connexion à Supabase"""
        try:
            load_dotenv()
            self.supabase_url = os.getenv('SUPABASE_URL')
            self.supabase_key = os.getenv('SUPABASE_KEY')
            
            if not self.supabase_url or not self.supabase_key:
                raise ValueError("Les variables d'environnement SUPABASE_URL et SUPABASE_KEY sont requises")
            
            self.supabase = create_client(self.supabase_url, self.supabase_key)
            logger.info("Connexion à Supabase établie avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de Supabase: {str(e)}")
            raise

    def sign_in(self, email: str, password: str) -> Dict:
        """Authentifie un utilisateur"""
        try:
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if hasattr(auth_response, 'user') and auth_response.user:
                # Récupérer le profil utilisateur
                user_id = auth_response.user.id
                profile = self.get_profile(user_id)
                
                return {
                    "success": True,
                    "data": {
                        "user": {
                            "id": user_id,
                            "email": auth_response.user.email,
                            "profile": profile
                        },
                        "session": {
                            "access_token": auth_response.session.access_token if auth_response.session else None,
                            "refresh_token": auth_response.session.refresh_token if auth_response.session else None
                        }
                    }
                }
            return {"success": False, "error": "Échec de l'authentification"}
            
        except Exception as e:
            logger.error(f"Erreur de connexion: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_profile(self, user_id: str) -> Dict:
        """Récupère le profil d'un utilisateur"""
        try:
            response = self.supabase.table('profiles').select('*').eq('user_id', user_id).single().execute()
            return response.data if response.data else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du profil: {str(e)}")
            return None

    def create_profile(self, user_id: str, profile_data: Dict) -> Dict:
        """Crée un profil utilisateur"""
        try:
            # Vérifier que l'utilisateur existe
            user = self.supabase.auth.admin.get_user_by_id(user_id)
            if not user:
                return {"success": False, "error": "Utilisateur non trouvé"}
            
            # Créer le profil
            response = self.supabase.table('profiles').insert({
                "user_id": user_id,
                "username": profile_data.get('username'),
                "full_name": profile_data.get('full_name'),
                "email": profile_data.get('email'),
                "is_admin": False
            }).execute()
            
            return {"success": True, "data": response.data[0] if response.data else None}
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du profil: {str(e)}")
            return {"success": False, "error": str(e)}

    def sign_up(self, email: str, password: str, options: dict = None) -> Dict:
        """Inscription d'un utilisateur"""
        try:
            # Créer l'utilisateur dans Supabase
            auth_response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                **(options or {})
            })
            
            if auth_response.user:
                return {
                    "success": True,
                    "data": {
                        "id": auth_response.user.id,
                        "email": auth_response.user.email,
                        "created_at": auth_response.user.created_at
                    }
                }
            
            return {"success": False, "error": "Erreur lors de l'inscription"}
            
        except Exception as e:
            logger.error(f"Erreur lors de l'inscription: {str(e)}")
            return {"success": False, "error": str(e)}

    def test_connection(self):
        """Teste la connexion à Supabase"""
        try:
            # Test simple : récupérer une catégorie
            self.supabase.table('categories').select('id').limit(1).execute()
            logger.info("Test de connexion réussi")
            return True
        except Exception as e:
            logger.error(f"Erreur lors du test de connexion: {str(e)}")
            return False
    
    def get_categories(self):
        """Récupère toutes les catégories"""
        try:
            response = self.supabase.table('categories').select('*').execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des catégories: {str(e)}")
            return []
    
    def get_category_by_slug(self, slug):
        """Récupère une catégorie par son slug"""
        try:
            response = self.supabase.table('categories')\
                .select('*')\
                .eq('slug', slug)\
                .limit(1)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la catégorie {slug}: {str(e)}")
            return None
    
    def get_brands(self):
        """Récupère toutes les marques"""
        try:
            response = self.supabase.table('brands').select('*').execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des marques: {str(e)}")
            return []
    
    def get_brand_by_slug(self, slug):
        """Récupère une marque par son slug"""
        try:
            response = self.supabase.table('brands')\
                .select('*')\
                .eq('slug', slug)\
                .limit(1)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la marque {slug}: {str(e)}")
            return None
    
    def get_products(self, category_id=None, brand_id=None, search=None):
        """Récupère les produits avec filtres optionnels"""
        try:
            query = self.supabase.table('products')\
                .select('*, categories!products_category_id_fkey(*), brands!products_brand_id_fkey(*)')
            
            if category_id:
                query = query.eq('category_id', category_id)
            if brand_id:
                query = query.eq('brand_id', brand_id)
            if search:
                query = query.ilike('name', f'%{search}%')
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des produits: {str(e)}")
            return []
    
    def get_product_by_slug(self, slug):
        """Récupère un produit par son slug"""
        try:
            response = self.supabase.table('products')\
                .select('*, categories!products_category_id_fkey(*), brands!products_brand_id_fkey(*)')\
                .eq('slug', slug)\
                .limit(1)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du produit {slug}: {str(e)}")
            return None
    
    def get_similar_products(self, product_id, limit=4):
        """Récupère des produits similaires"""
        try:
            # D'abord, obtenir la catégorie du produit
            product = self.supabase.table('products')\
                .select('category_id')\
                .eq('id', product_id)\
                .limit(1)\
                .execute()
            
            if not product.data:
                return []
            
            category_id = product.data[0]['category_id']
            
            # Récupérer d'autres produits de la même catégorie
            response = self.supabase.table('products')\
                .select('*, categories!products_category_id_fkey(*), brands!products_brand_id_fkey(*)')\
                .eq('category_id', category_id)\
                .neq('id', product_id)\
                .limit(limit)\
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des produits similaires: {str(e)}")
            return []
    
    def get_user_orders(self, user_id):
        """Récupère les commandes d'un utilisateur"""
        try:
            response = self.supabase.table('orders')\
                .select('*, order_items(*)')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des commandes: {str(e)}")
            return []

    # Méthodes d'authentification
    def sign_out(self) -> Dict:
        """Déconnexion de l'utilisateur"""
        try:
            self.supabase.auth.sign_out()
            return {"success": True}
        except Exception as e:
            return self._handle_error("de la déconnexion", e)

    def get_user(self) -> Dict:
        """Récupère l'utilisateur actuellement connecté"""
        try:
            user = self.supabase.auth.get_user()
            if not user:
                return {"success": False, "error": "Aucun utilisateur connecté"}
            
            return {
                "success": True,
                "data": {
                    "user": user
                }
            }
        except Exception as e:
            return self._handle_error("de la récupération de l'utilisateur", e)

    def update_user_profile(self, user_id: str, profile_data: Dict) -> Dict:
        """Met à jour le profil d'un utilisateur"""
        try:
            # Mettre à jour les métadonnées de l'utilisateur
            auth_response = self.supabase.auth.admin.update_user_by_id(
                user_id,
                {"user_metadata": profile_data}
            )
            
            if not auth_response.user:
                return {"success": False, "error": "Profil non trouvé"}
            
            return {"success": True, "data": auth_response.user}
        except Exception as e:
            return self._handle_error("de la mise à jour du profil", e)

    # Fonctions pour les produits
    def get_products(self) -> List[Dict]:
        """Récupère tous les produits"""
        try:
            response = self.supabase.table('products').select('*').execute()
            return response.data
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des produits: {str(e)}")
            raise

    def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """Récupère un produit par son ID"""
        try:
            response = self.supabase.table('products').select('*').eq('id', product_id).single().execute()
            return response.data
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du produit {product_id}: {str(e)}")
            return None

    def create_product(self, product_data: Dict) -> Dict:
        """Crée un nouveau produit"""
        try:
            # Ajout d'un slug basé sur le nom du produit
            if 'name' in product_data:
                product_data['slug'] = slugify(product_data['name'])
            
            # Ajout de la date de création
            product_data['created_at'] = datetime.utcnow().isoformat()
            
            response = self.supabase.table('products').insert(product_data).execute()
            return response.data[0]
        except Exception as e:
            logger.error(f"Erreur lors de la création du produit: {str(e)}")
            raise

    def update_product(self, product_id: str, product_data: Dict) -> Optional[Dict]:
        """Met à jour un produit existant"""
        try:
            # Mise à jour du slug si le nom est modifié
            if 'name' in product_data:
                product_data['slug'] = slugify(product_data['name'])
            
            # Ajout de la date de mise à jour
            product_data['updated_at'] = datetime.utcnow().isoformat()
            
            response = self.supabase.table('products').update(product_data).eq('id', product_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du produit {product_id}: {str(e)}")
            raise

    # Fonctions pour les catégories
    def get_categories_with_count(self):
        """Récupère les catégories avec le nombre de produits"""
        try:
            # Récupérer toutes les catégories
            categories = self.supabase.table('categories')\
                .select('*')\
                .execute()

            if not categories.data:
                return {"success": True, "data": []}

            # Pour chaque catégorie, compter le nombre de produits
            for category in categories.data:
                count = self.supabase.table('products')\
                    .select('count')\
                    .eq('category_id', category['id'])\
                    .eq('is_active', True)\
                    .execute()
                category['product_count'] = count.count

            return {"success": True, "data": categories.data}
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des catégories: {str(e)}")
            return {"success": False, "error": str(e), "data": []}

    def get_categories(self):
        """Récupère toutes les catégories"""
        try:
            response = self.supabase.table('categories').select("*").execute()
            categories = []
            for item in response.data:
                if isinstance(item, dict):
                    categories.append(item)
                else:
                    logger.warning(f"Format de données inattendu pour la catégorie: {item}")
            
            return categories
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des catégories: {str(e)}")
            return []

    # Fonctions pour les marques
    def get_brands_with_count(self):
        """Récupère les marques avec le nombre de produits"""
        try:
            # Récupérer toutes les marques
            brands = self.supabase.table('brands')\
                .select('*')\
                .execute()

            if not brands.data:
                return {"success": True, "data": []}

            # Pour chaque marque, compter le nombre de produits
            for brand in brands.data:
                count = self.supabase.table('products')\
                    .select('count')\
                    .eq('brand_id', brand['id'])\
                    .eq('is_active', True)\
                    .execute()
                brand['product_count'] = count.count

            return {"success": True, "data": brands.data}
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des marques: {str(e)}")
            return {"success": False, "error": str(e), "data": []}

    def get_brands(self):
        """Récupère toutes les marques"""
        try:
            response = self.supabase.table('brands').select("*").execute()
            return response.data
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des marques: {str(e)}")
            return []

    def create_category(self, data: Dict) -> Dict:
        """Crée une nouvelle catégorie"""
        try:
            data['slug'] = slugify(data['name'])
            data['created_at'] = datetime.utcnow().isoformat()
            data['updated_at'] = data['created_at']
            
            response = self.supabase.table('categories')\
                .insert(data)\
                .execute()
            
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return self._handle_error("de la création de la catégorie", e)

    def create_brand(self, data: Dict) -> Dict:
        """Crée une nouvelle marque"""
        try:
            data['slug'] = slugify(data['name'])
            data['created_at'] = datetime.utcnow().isoformat()
            data['updated_at'] = data['created_at']
            
            response = self.supabase.table('brands')\
                .insert(data)\
                .execute()
            
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return self._handle_error("de la création de la marque", e)

    def get_product_by_slug(self, slug):
        """Récupère un produit par son slug"""
        try:
            response = self.supabase.table('products')\
                .select('*, category:categories(*), brand:brands(*)')\
                .eq('slug', slug)\
                .single()\
                .execute()
            
            if not response.data:
                return {"success": False, "error": f"Produit avec le slug '{slug}' non trouvé"}
            
            return {"success": True, "data": response.data}
        except Exception as e:
            return self._handle_error(f"de la récupération du produit avec le slug '{slug}'", e)

    def get_products(self):
        """Récupère tous les produits"""
        try:
            response = self.supabase.table('products')\
                .select('*, categories!products_category_id_fkey(*), brands!products_brand_id_fkey(*)')\
                .execute()
            return response.data
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des produits: {str(e)}")
            return []

    def get_reviews_by_product(self, product_id):
        """Récupère tous les avis pour un produit"""
        try:
            response = self.supabase.table('reviews')\
                .select('*, user:auth.users!reviews_user_id_fkey(*)')\
                .eq('product_id', product_id)\
                .order('created_at', desc=True)\
                .execute()
            return response.data
        except Exception as e:
            return self._handle_error("de la récupération des avis", e)

    def create_review(self, review_data):
        """Crée un nouvel avis"""
        try:
            # Ajouter les timestamps
            review_data['created_at'] = datetime.utcnow().isoformat()
            review_data['updated_at'] = review_data['created_at']
            
            response = self.supabase.table('reviews')\
                .insert(review_data)\
                .execute()
            
            if not response.data:
                return {"success": False, "error": "Erreur lors de la création de l'avis"}
            
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return self._handle_error("de la création de l'avis", e)

    def update_review(self, review_id, user_id, review_data):
        """Met à jour un avis existant"""
        try:
            # Mettre à jour le timestamp
            review_data['updated_at'] = datetime.utcnow().isoformat()
            
            response = self.supabase.table('reviews')\
                .update(review_data)\
                .eq('id', review_id)\
                .eq('user_id', user_id)\
                .execute()
            
            if not response.data:
                return {"success": False, "error": "Avis non trouvé ou non autorisé"}
            
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return self._handle_error("de la mise à jour de l'avis", e)

    def delete_review(self, review_id, user_id):
        """Supprime un avis"""
        try:
            response = self.supabase.table('reviews')\
                .delete()\
                .eq('id', review_id)\
                .eq('user_id', user_id)\
                .execute()
            
            if not response.data:
                return {"success": False, "error": "Avis non trouvé ou non autorisé"}
            
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return self._handle_error("de la suppression de l'avis", e)

    def get_products_by_category(self, category_id, limit=None, exclude_id=None):
        query = self.supabase.table('products').select('*').eq('category_id', category_id)
        
        if exclude_id:
            query = query.neq('id', exclude_id)
        
        if limit:
            query = query.limit(limit)
        
        response = query.execute()
        return response.data if response.data else []

    def get_user_notifications(self, user_id):
        """Récupère les notifications d'un utilisateur"""
        response = self.supabase.table('notifications')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .limit(10)\
            .execute()
        return response.data if response.data else []

    def get_user_cart(self, user_id):
        """Récupère le panier d'un utilisateur"""
        response = self.supabase.table('cart_items')\
            .select('*, product:products(*)')\
            .eq('user_id', user_id)\
            .execute()
        
        if not response.data:
            return {'items': [], 'total_items': 0, 'total_price': 0}
        
        items = response.data
        total_items = sum(item.get('quantity', 0) for item in items)
        total_price = sum(item.get('quantity', 0) * item.get('product', {}).get('price', 0) for item in items)
        
        return {
            'items': items,
            'total_items': total_items,
            'total_price': total_price
        }

    def get_promotions(self):
        """Récupère la liste des promotions actives"""
        response = self.supabase.table('promotions')\
            .select('*, product:products(*)')\
            .eq('active', True)\
            .order('created_at', desc=True)\
            .execute()
        return response.data if response.data else []

    def get_notifications(self, user_id: str, limit: int = 10, offset: int = 0) -> Dict:
        """Récupère les notifications d'un utilisateur"""
        try:
            response = self.supabase.table('notifications') \
                .select('*') \
                .eq('user_id', user_id) \
                .order('created_at', desc=True) \
                .limit(limit) \
                .offset(offset) \
                .execute()
            
            return {
                "success": True,
                "data": response.data
            }
        except Exception as e:
            return self._handle_error("de la récupération des notifications", e)

    def mark_notification_as_read(self, notification_id: str, user_id: str) -> Dict:
        """Marque une notification comme lue"""
        try:
            response = self.supabase.table('notifications') \
                .update({'read': True}) \
                .eq('id', notification_id) \
                .eq('user_id', user_id) \
                .execute()
            
            return {
                "success": True,
                "data": response.data[0] if response.data else None
            }
        except Exception as e:
            return self._handle_error("du marquage de la notification comme lue", e)

    def create_notification(self, user_id: str, title: str, message: str, type: str = 'info') -> Dict:
        """Crée une nouvelle notification"""
        try:
            response = self.supabase.table('notifications') \
                .insert({
                    'user_id': user_id,
                    'title': title,
                    'message': message,
                    'type': type,
                    'read': False
                }) \
                .execute()
            
            return {
                "success": True,
                "data": response.data[0] if response.data else None
            }
        except Exception as e:
            return self._handle_error("de la création de la notification", e)

    def create_order(self, user_id: str, items: List[Dict]) -> Dict:
        """Crée une nouvelle commande avec ses items"""
        try:
            # Validation des items
            if not items:
                return {"success": False, "error": "La commande doit contenir au moins un article"}
            
            # Calculer le montant total et vérifier le stock
            total_amount = 0
            for item in items:
                product = self.get_product_by_id(item['product_id'])
                if not product['success']:
                    return {"success": False, "error": f"Produit {item['product_id']} introuvable"}
                
                if product['data']['stock'] < item['quantity']:
                    return {"success": False, "error": f"Stock insuffisant pour {product['data']['name']}"}
                
                total_amount += product['data']['price'] * item['quantity']
            
            # Créer la commande
            order_data = {
                'user_id': user_id,
                'total_amount': total_amount,
                'status': 'pending',
                'created_at': datetime.utcnow().isoformat()
            }
            
            order_response = self.supabase.table('orders')\
                .insert(order_data)\
                .execute()
            
            if not order_response.data:
                return {"success": False, "error": "Erreur lors de la création de la commande"}
            
            order_id = order_response.data[0]['id']
            
            # Créer les items de la commande
            order_items = [{
                'order_id': order_id,
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'price': self.get_product_by_id(item['product_id'])['data']['price'],
                'created_at': datetime.utcnow().isoformat()
            } for item in items]
            
            items_response = self.supabase.table('order_items')\
                .insert(order_items)\
                .execute()
            
            # Mettre à jour le stock des produits
            for item in items:
                product = self.get_product_by_id(item['product_id'])['data']
                self.update_product(item['product_id'], {
                    'stock': product['stock'] - item['quantity']
                })
            
            # Créer une notification pour l'utilisateur
            self.create_notification(
                user_id=user_id,
                title="Nouvelle commande",
                message=f"Votre commande #{order_id} a été créée avec succès",
                type="order"
            )
            
            return {
                "success": True,
                "data": {
                    "order": order_response.data[0],
                    "items": items_response.data
                }
            }
        except Exception as e:
            return self._handle_error("de la création de la commande", e)

    def get_user_orders(self, user_id: str, limit: int = 10, offset: int = 0) -> Dict:
        """Récupère les commandes d'un utilisateur"""
        try:
            response = self.supabase.table('orders')\
                .select('*, order_items(*, product:products(*))')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .range(offset, offset + limit - 1)\
                .execute()
            
            return {"success": True, "data": response.data}
        except Exception as e:
            return self._handle_error("de la récupération des commandes", e)

    def get_order_details(self, order_id: str, user_id: str) -> Dict:
        """Récupère les détails d'une commande spécifique"""
        try:
            response = self.supabase.table('orders')\
                .select('*, order_items(*, product:products(*))')\
                .eq('id', order_id)\
                .eq('user_id', user_id)\
                .single()\
                .execute()
            
            if not response.data:
                return {"success": False, "error": "Commande non trouvée"}
            
            return {"success": True, "data": response.data}
        except Exception as e:
            return self._handle_error("de la récupération des détails de la commande", e)

    def update_order_status(self, order_id: str, user_id: str, status: str) -> Dict:
        """Met à jour le statut d'une commande"""
        try:
            # Vérifier que le statut est valide
            valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            if status not in valid_statuses:
                return {"success": False, "error": "Statut invalide"}
            
            # Vérifier que la commande appartient à l'utilisateur
            order = self.get_order_details(order_id, user_id)
            if not order['success']:
                return order
            
            response = self.supabase.table('orders')\
                .update({'status': status, 'updated_at': datetime.utcnow().isoformat()})\
                .eq('id', order_id)\
                .eq('user_id', user_id)\
                .execute()
            
            # Créer une notification pour le changement de statut
            self.create_notification(
                user_id=user_id,
                title="Statut de commande mis à jour",
                message=f"Le statut de votre commande #{order_id} est maintenant : {status}",
                type="order_status"
            )
            
            return {"success": True, "data": response.data[0]}
        except Exception as e:
            return self._handle_error("de la mise à jour du statut de la commande", e)

    def get_user_statistics(self, user_id):
        """Récupère les statistiques de l'utilisateur."""
        try:
            # Nombre total de commandes
            total_orders = self.supabase.table('orders')\
                .select('id')\
                .eq('user_id', user_id)\
                .execute()

            # Montant total dépensé
            total_spent = self.supabase.table('orders')\
                .select('total_amount')\
                .eq('user_id', user_id)\
                .execute()

            # Commandes récentes (30 derniers jours)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_orders = self.supabase.table('orders')\
                .select('*')\
                .eq('user_id', user_id)\
                .gte('created_at', thirty_days_ago.isoformat())\
                .execute()

            # Produits les plus commandés
            most_ordered = self.supabase.table('order_items')\
                .select('product_id, quantity')\
                .eq('user_id', user_id)\
                .execute()

            # Statuts des commandes
            order_statuses = self.supabase.table('orders')\
                .select('status')\
                .eq('user_id', user_id)\
                .execute()

            # Traitement des résultats
            total_orders_count = len(total_orders.data) if total_orders.data else 0
            total_spent_amount = sum(order['total_amount'] for order in total_spent.data) if total_spent.data else 0
            recent_orders_count = len(recent_orders.data) if recent_orders.data else 0

            # Calcul des statuts
            status_counts = {}
            if order_statuses.data:
                for order in order_statuses.data:
                    status = order['status']
                    status_counts[status] = status_counts.get(status, 0) + 1

            # Calcul des produits les plus commandés
            product_quantities = {}
            if most_ordered.data:
                for item in most_ordered.data:
                    product_id = item['product_id']
                    quantity = item['quantity']
                    product_quantities[product_id] = product_quantities.get(product_id, 0) + quantity

            # Récupération des détails des produits les plus commandés
            top_products = []
            if product_quantities:
                top_product_ids = sorted(product_quantities.items(), key=lambda x: x[1], reverse=True)[:5]
                for product_id, quantity in top_product_ids:
                    product = self.supabase.table('products')\
                        .select('name')\
                        .eq('id', product_id)\
                        .single()\
                        .execute()
                    if product.data:
                        top_products.append({
                            'name': product.data['name'],
                            'quantity': quantity
                        })

            return {
                'success': True,
                'data': {
                    'total_orders': total_orders_count,
                    'total_spent': total_spent_amount,
                    'recent_orders': recent_orders_count,
                    'status_distribution': status_counts,
                    'top_products': top_products,
                    'recent_activity': recent_orders.data if recent_orders.data else []
                }
            }

        except Exception as e:
            logging.error(f"Erreur lors de la récupération des statistiques: {str(e)}")
            return {
                'success': False,
                'error': "Erreur lors de la récupération des statistiques"
            }

    def create_stock_alert(self, alert_data: Dict) -> Dict:
        """Crée une nouvelle alerte de stock"""
        try:
            result = self.supabase.table('stock_alerts').insert(alert_data).execute()
            
            if not result.data:
                return {"success": False, "error": "Erreur lors de la création de l'alerte"}
            
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return self._handle_error("de la création de l'alerte de stock", e)

    def get_stock_alerts(self, user_id: str = None, is_active: bool = True) -> Dict:
        """Récupère les alertes de stock avec filtres"""
        try:
            query = self.supabase.table('stock_alerts').select("""
                *,
                product:products (
                    id,
                    name,
                    stock,
                    price,
                    image_url
                )
            """)

            if user_id:
                query = query.eq('user_id', user_id)
            if is_active is not None:
                query = query.eq('is_active', is_active)

            result = query.execute()
            
            if not result.data:
                return {
                    "success": True,
                    "data": []
                }
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return self._handle_error("de la récupération des alertes de stock", e)

    def update_stock_alert(self, alert_id: str, update_data: Dict) -> Dict:
        """Met à jour une alerte de stock"""
        try:
            result = self.supabase.table('stock_alerts').update(
                update_data
            ).eq('id', alert_id).execute()
            
            if not result.data:
                return {"success": False, "error": "Alerte non trouvée"}
            
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return self._handle_error("de la mise à jour de l'alerte de stock", e)

    def process_stock_alerts(self) -> Dict:
        """Traite toutes les alertes de stock actives"""
        try:
            # Récupérer toutes les alertes actives avec les informations des produits
            alerts = self.get_stock_alerts(is_active=True)
            
            if not alerts["success"]:
                return alerts
            
            processed_alerts = []
            for alert in alerts["data"]:
                product = alert.get("product")
                if not product:
                    continue
                
                # Vérifier si le stock est en dessous du seuil
                if product["stock"] <= alert["threshold"]:
                    # Créer une notification
                    notification_data = {
                        "user_id": alert["user_id"],
                        "type": "stock_alert",
                        "title": f"Alerte de stock : {product['name']}",
                        "message": f"Le stock de {product['name']} est bas ({product['stock']} unités restantes)",
                        "data": {
                            "product_id": product["id"],
                            "current_stock": product["stock"],
                            "threshold": alert["threshold"]
                        }
                    }
                    
                    notification_result = self.create_notification(notification_data)
                    if notification_result["success"]:
                        processed_alerts.append({
                            "alert_id": alert["id"],
                            "notification_id": notification_result["data"]["id"]
                        })
            
            return {
                "success": True,
                "processed_alerts": processed_alerts
            }
        except Exception as e:
            return self._handle_error("du traitement des alertes de stock", e)

    def get_user_statistics(self, user_id):
        """Récupère les statistiques de l'utilisateur."""
        try:
            # Nombre total de commandes
            total_orders = self.supabase.table('orders')\
                .select('id')\
                .eq('user_id', user_id)\
                .execute()

            # Montant total dépensé
            total_spent = self.supabase.table('orders')\
                .select('total_amount')\
                .eq('user_id', user_id)\
                .execute()

            # Commandes récentes (30 derniers jours)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_orders = self.supabase.table('orders')\
                .select('*')\
                .eq('user_id', user_id)\
                .gte('created_at', thirty_days_ago.isoformat())\
                .execute()

            # Produits les plus commandés
            most_ordered = self.supabase.table('order_items')\
                .select('product_id, quantity')\
                .eq('user_id', user_id)\
                .execute()

            # Statuts des commandes
            order_statuses = self.supabase.table('orders')\
                .select('status')\
                .eq('user_id', user_id)\
                .execute()

            # Traitement des résultats
            total_orders_count = len(total_orders.data) if total_orders.data else 0
            total_spent_amount = sum(order['total_amount'] for order in total_spent.data) if total_spent.data else 0
            recent_orders_count = len(recent_orders.data) if recent_orders.data else 0

            # Calcul des statuts
            status_counts = {}
            if order_statuses.data:
                for order in order_statuses.data:
                    status = order['status']
                    status_counts[status] = status_counts.get(status, 0) + 1

            # Calcul des produits les plus commandés
            product_quantities = {}
            if most_ordered.data:
                for item in most_ordered.data:
                    product_id = item['product_id']
                    quantity = item['quantity']
                    product_quantities[product_id] = product_quantities.get(product_id, 0) + quantity

            # Récupération des détails des produits les plus commandés
            top_products = []
            if product_quantities:
                top_product_ids = sorted(product_quantities.items(), key=lambda x: x[1], reverse=True)[:5]
                for product_id, quantity in top_product_ids:
                    product = self.supabase.table('products')\
                        .select('name')\
                        .eq('id', product_id)\
                        .single()\
                        .execute()
                    if product.data:
                        top_products.append({
                            'name': product.data['name'],
                            'quantity': quantity
                        })

            return {
                'success': True,
                'data': {
                    'total_orders': total_orders_count,
                    'total_spent': total_spent_amount,
                    'recent_orders': recent_orders_count,
                    'status_distribution': status_counts,
                    'top_products': top_products,
                    'recent_activity': recent_orders.data if recent_orders.data else []
                }
            }

        except Exception as e:
            logging.error(f"Erreur lors de la récupération des statistiques: {str(e)}")
            return {
                'success': False,
                'error': "Erreur lors de la récupération des statistiques"
            }

    def create_stock_alert(self, product_id: str, alert_type: str, message: str, current_stock: int, threshold: int) -> dict:
        """Crée une alerte de stock."""
        try:
            alert_data = {
                'product_id': product_id,
                'type': alert_type,
                'message': message,
                'current_stock': current_stock,
                'threshold': threshold,
                'status': 'pending'
            }
            
            response = self.supabase.table('stock_alerts').insert(alert_data).execute()
            
            # Créer une notification pour les admins
            notification_data = {
                'title': f'Alerte de stock - {alert_type}',
                'message': message,
                'type': 'stock_alert',
                'reference_id': response.data[0]['id'],
                'is_read': False
            }
            self.create_admin_notification(notification_data)
            
            return {'success': True, 'data': response.data[0]}
        except Exception as e:
            return self._handle_error("de la création de l'alerte de stock", e)

    def get_stock_alerts(self, status: str = None, limit: int = 50) -> dict:
        """Récupère les alertes de stock."""
        try:
            query = self.supabase.table('stock_alerts')\
                .select('*, products(name)')\
                .order('created_at', desc=True)\
                .limit(limit)

            if status:
                query = query.eq('status', status)

            response = query.execute()
            return {'success': True, 'data': response.data}
        except Exception as e:
            return self._handle_error("de la récupération des alertes de stock", e)

    def update_stock_alert_status(self, alert_id: str, status: str, user_id: str) -> dict:
        """Met à jour le statut d'une alerte de stock."""
        try:
            update_data = {
                'status': status,
                'processed_at': datetime.now().isoformat(),
                'processed_by': user_id
            }
            
            response = self.supabase.table('stock_alerts')\
                .update(update_data)\
                .eq('id', alert_id)\
                .execute()
                
            return {'success': True, 'data': response.data[0]}
        except Exception as e:
            return self._handle_error("de la mise à jour du statut de l'alerte", e)

    def check_stock_levels(self) -> dict:
        """Vérifie les niveaux de stock et crée des alertes si nécessaire."""
        try:
            # Récupérer tous les produits actifs
            products = self.supabase.table('products')\
                .select('id, name, stock, min_stock, max_stock')\
                .eq('is_active', True)\
                .execute()

            alerts_created = []
            for product in products.data:
                current_stock = product['stock']
                min_stock = product['min_stock']
                max_stock = product['max_stock']

                # Alerte de stock bas
                if current_stock <= min_stock:
                    alert = self.create_stock_alert(
                        product_id=product['id'],
                        alert_type='low_stock',
                        message=f"Stock bas pour {product['name']} ({current_stock} unités restantes)",
                        current_stock=current_stock,
                        threshold=min_stock
                    )
                    if alert['success']:
                        alerts_created.append(alert['data'])

                # Alerte de rupture de stock
                if current_stock == 0:
                    alert = self.create_stock_alert(
                        product_id=product['id'],
                        alert_type='out_of_stock',
                        message=f"Rupture de stock pour {product['name']}",
                        current_stock=current_stock,
                        threshold=0
                    )
                    if alert['success']:
                        alerts_created.append(alert['data'])

                # Alerte de surstock
                if max_stock and current_stock >= max_stock:
                    alert = self.create_stock_alert(
                        product_id=product['id'],
                        alert_type='overstock',
                        message=f"Surstock pour {product['name']} ({current_stock} unités)",
                        current_stock=current_stock,
                        threshold=max_stock
                    )
                    if alert['success']:
                        alerts_created.append(alert['data'])

            return {
                'success': True,
                'data': {
                    'alerts_created': len(alerts_created),
                    'alerts': alerts_created
                }
            }
        except Exception as e:
            return self._handle_error("de la vérification des niveaux de stock", e)

    def create_admin_notification(self, notification_data: dict) -> dict:
        """Crée une notification pour tous les administrateurs."""
        try:
            # Récupérer tous les utilisateurs admin
            admins = self.supabase.rpc('get_admin_users').execute()
            
            notifications = []
            for admin in admins.data:
                notification = {
                    **notification_data,
                    'user_id': admin['id']
                }
                response = self.supabase.table('notifications').insert(notification).execute()
                notifications.extend(response.data)

            return {'success': True, 'data': notifications}
        except Exception as e:
            return self._handle_error("de la création des notifications admin", e)

    # Gestion des catégories
    def create_category(self, data: dict) -> dict:
        """Crée une nouvelle catégorie."""
        try:
            # Générer le slug
            data['slug'] = self._generate_slug(data['name'])
            
            # Upload de l'image si présente
            if 'image' in data:
                image_url = self._upload_file(
                    data['image'],
                    f"categories/{data['slug']}",
                    content_type=data['image'].content_type
                )
                data['image_url'] = image_url
                del data['image']
            
            response = self.supabase.table('categories').insert(data).execute()
            return {'success': True, 'data': response.data[0]}
        except Exception as e:
            return self._handle_error("de la création de la catégorie", e)

    def update_category(self, category_id: str, data: dict) -> dict:
        """Met à jour une catégorie."""
        try:
            update_data = data.copy()
            
            # Mise à jour du slug si le nom change
            if 'name' in update_data:
                update_data['slug'] = self._generate_slug(update_data['name'])
            
            # Upload de la nouvelle image si présente
            if 'image' in update_data:
                image_url = self._upload_file(
                    update_data['image'],
                    f"categories/{update_data.get('slug', '')}",
                    content_type=update_data['image'].content_type
                )
                update_data['image_url'] = image_url
                del update_data['image']
            
            response = self.supabase.table('categories')\
                .update(update_data)\
                .eq('id', category_id)\
                .execute()
            
            return {'success': True, 'data': response.data[0]}
        except Exception as e:
            return self._handle_error("de la mise à jour de la catégorie", e)

    def get_categories(self, parent_id: str = None, include_inactive: bool = False) -> dict:
        """Récupère la liste des catégories."""
        try:
            query = self.supabase.table('categories')\
                .select('*')\
                .order('name')
            
            if not include_inactive:
                query = query.eq('is_active', True)
            
            if parent_id:
                query = query.eq('parent_id', parent_id)
            else:
                query = query.is_('parent_id', 'null')
            
            response = query.execute()
            return {'success': True, 'data': response.data}
        except Exception as e:
            return self._handle_error("de la récupération des catégories", e)

    def get_category_tree(self) -> dict:
        """Récupère l'arborescence complète des catégories."""
        try:
            categories = self.get_categories(include_inactive=True)
            if not categories['success']:
                return categories
            
            def build_tree(parent_id=None):
                return [
                    {
                        **cat,
                        'children': build_tree(cat['id'])
                    }
                    for cat in categories['data']
                    if cat['parent_id'] == parent_id
                ]
            
            tree = build_tree()
            return {'success': True, 'data': tree}
        except Exception as e:
            return self._handle_error("de la récupération de l'arborescence", e)

    # Gestion des produits
    def create_product(self, data: dict) -> dict:
        """Crée un nouveau produit."""
        try:
            # Générer le slug
            data['slug'] = self._generate_slug(data['name'])
            
            # Gestion des images
            if 'image' in data:
                image_url = self._upload_file(
                    data['image'],
                    f"products/{data['slug']}/main",
                    content_type=data['image'].content_type
                )
                data['image_url'] = image_url
                del data['image']
            
            if 'additional_images' in data:
                additional_urls = []
                for idx, img in enumerate(data['additional_images']):
                    url = self._upload_file(
                        img,
                        f"products/{data['slug']}/additional_{idx}",
                        content_type=img.content_type
                    )
                    additional_urls.append(url)
                data['additional_images'] = additional_urls
            
            # Créer le produit
            response = self.supabase.table('products').insert(data).execute()
            product = response.data[0]
            
            # Créer une entrée dans stock_movements
            self._create_initial_stock_movement(
                product['id'],
                data.get('stock', 0),
                data.get('created_by')
            )
            
            return {'success': True, 'data': product}
        except Exception as e:
            return self._handle_error("de la création du produit", e)

    def update_product(self, product_id: str, data: dict) -> dict:
        """Met à jour un produit."""
        try:
            update_data = data.copy()
            
            # Mise à jour du slug si le nom change
            if 'name' in update_data:
                update_data['slug'] = self._generate_slug(update_data['name'])
            
            # Gestion des images
            if 'image' in update_data:
                image_url = self._upload_file(
                    update_data['image'],
                    f"products/{update_data.get('slug', '')}/main",
                    content_type=update_data['image'].content_type
                )
                update_data['image_url'] = image_url
                del update_data['image']
            
            if 'additional_images' in update_data:
                additional_urls = []
                for idx, img in enumerate(update_data['additional_images']):
                    url = self._upload_file(
                        img,
                        f"products/{update_data.get('slug', '')}/additional_{idx}",
                        content_type=img.content_type
                    )
                    additional_urls.append(url)
                update_data['additional_images'] = additional_urls
            
            # Vérifier si le stock change
            old_product = self.get_product(product_id)
            if old_product['success'] and 'stock' in update_data:
                old_stock = old_product['data']['stock']
                new_stock = update_data['stock']
                
                if old_stock != new_stock:
                    self._create_stock_movement(
                        product_id=product_id,
                        quantity=new_stock - old_stock,
                        type='adjustment',
                        reason='Mise à jour manuelle',
                        previous_stock=old_stock,
                        created_by=update_data.get('updated_by')
                    )
            
            response = self.supabase.table('products')\
                .update(update_data)\
                .eq('id', product_id)\
                .execute()
            
            return {'success': True, 'data': response.data[0]}
        except Exception as e:
            return self._handle_error("de la mise à jour du produit", e)

    def get_products(self, category_id: str = None, brand_id: str = None,
                    search: str = None, include_inactive: bool = False,
                    page: int = 1, per_page: int = 20) -> dict:
        """Récupère la liste des produits avec filtres et pagination."""
        try:
            logger.info(f"Récupération des produits avec les filtres: category={category_id}, brand={brand_id}, search={search}")
            
            # Construire la requête de base avec tous les champs nécessaires
            query = """
                *,
                category:categories (
                    id,
                    name,
                    slug,
                    description
                ),
                brand:brands (
                    id,
                    name,
                    slug,
                    description
                )
            """
            
            base_query = self.supabase.table('products').select(query)

            # Appliquer les filtres
            if not include_inactive:
                base_query = base_query.eq('is_active', True)
            
            if category_id:
                base_query = base_query.eq('category_id', category_id)
            
            if brand_id:
                base_query = base_query.eq('brand_id', brand_id)
            
            if search:
                base_query = base_query.or_(f"name.ilike.%{search}%,description.ilike.%{search}%")
            
            # Tri
            if sort == 'price_asc':
                base_query = base_query.order('price', desc=False)
            elif sort == 'price_desc':
                base_query = base_query.order('price', desc=True)
            else:
                base_query = base_query.order('name')
            
            # Pagination
            start = (page - 1) * per_page
            base_query = base_query.range(start, start + per_page - 1)
            
            response = base_query.execute()
            
            # Récupérer le nombre total pour la pagination
            count_response = self.supabase.table('products')\
                .select('id', count='exact')\
                .execute()
            
            total = count_response.count
            
            return {
                'success': True,
                'data': {
                    'products': response.data,
                    'pagination': {
                        'total': total,
                        'page': page,
                        'per_page': per_page,
                        'total_pages': -(-total // per_page)  # Ceiling division
                    }
                }
            }
            
        except Exception as e:
            return self._handle_error("de la récupération des produits", e)

    def get_product(self, product_id: str) -> dict:
        """Récupère les détails d'un produit."""
        try:
            response = self.supabase.table('products')\
                .select('*, categories(name), brands(name)')\
                .eq('id', product_id)\
                .single()\
                .execute()
            
            return {'success': True, 'data': response.data}
        except Exception as e:
            return self._handle_error("de la récupération du produit", e)

    # Méthodes utilitaires
    def _generate_slug(self, name: str) -> str:
        """Génère un slug unique à partir d'un nom."""
        base_slug = name.lower()\
            .replace(' ', '-')\
            .replace('_', '-')\
            .replace('/', '-')\
            .replace('\\', '-')
        
        # Supprimer les caractères spéciaux
        import re
        base_slug = re.sub(r'[^a-z0-9-]', '', base_slug)
        
        # Vérifier l'unicité
        slug = base_slug
        counter = 1
        
        while True:
            # Vérifier si le slug existe déjà
            exists = self.supabase.table('products')\
                .select('id')\
                .eq('slug', slug)\
                .execute()
            
            if not exists.data:
                break
            
            # Ajouter un compteur si le slug existe
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug

    def _create_initial_stock_movement(self, product_id: str, quantity: int, created_by: str) -> dict:
        """Crée le mouvement de stock initial pour un nouveau produit."""
        return self._create_stock_movement(
            product_id=product_id,
            quantity=quantity,
            type='in',
            reason='Stock initial',
            previous_stock=0,
            created_by=created_by
        )

    def _create_stock_movement(self, product_id: str, quantity: int,
                             type: str, reason: str, previous_stock: int,
                             created_by: str) -> dict:
        """Crée un mouvement de stock."""
        try:
            movement_data = {
                'product_id': product_id,
                'quantity': quantity,
                'type': type,
                'reason': reason,
                'previous_stock': previous_stock,
                'new_stock': previous_stock + quantity,
                'created_by': created_by
            }
            
            response = self.supabase.table('stock_movements')\
                .insert(movement_data)\
                .execute()
            
            return {'success': True, 'data': response.data[0]}
        except Exception as e:
            return self._handle_error("de la création du mouvement de stock", e)

    def _upload_file(self, file, path: str, content_type: str = None) -> str:
        """Upload un fichier vers Supabase Storage."""
        try:
            # Lire le contenu du fichier
            file_content = file.read()
            
            # Upload vers Supabase Storage
            response = self.supabase.storage\
                .from_('media')\
                .upload(
                    path,
                    file_content,
                    {'content-type': content_type} if content_type else None
                )
            
            # Construire l'URL publique
            public_url = self.supabase.storage\
                .from_('media')\
                .get_public_url(path)
            
            return public_url
        except Exception as e:
            raise Exception(f"Erreur lors de l'upload du fichier : {str(e)}")

    def get_categories(self) -> List:
        """Récupère toutes les catégories"""
        try:
            response = self.supabase.table('categories')\
                .select('*')\
                .execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des catégories: {str(e)}")
            return []

    def get_brands(self) -> List:
        """Récupère toutes les marques"""
        try:
            response = self.supabase.table('brands')\
                .select('*')\
                .execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des marques: {str(e)}")
            return []

    def get_products(self) -> List:
        """Récupère tous les produits"""
        try:
            response = self.supabase.table('products')\
                .select('*, categories!products_category_id_fkey(*), brands!products_brand_id_fkey(*)')\
                .execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des produits: {str(e)}")
            return []
def init_tables(self):
    """Initialize tables in Supabase"""
    try:
        # Create tables using Supabase's SQL editor
        queries = [
            """
            CREATE TABLE IF NOT EXISTS categories (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR(255) NOT NULL,
                slug VARCHAR(255) NOT NULL UNIQUE,
                description TEXT,
                image_url TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS brands (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR(255) NOT NULL,
                slug VARCHAR(255) NOT NULL UNIQUE,
                description TEXT,
                logo_url TEXT,
                website_url TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name VARCHAR(255) NOT NULL,
                slug VARCHAR(255) NOT NULL UNIQUE,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                category_id UUID REFERENCES categories(id),
                brand_id UUID REFERENCES brands(id),
                image_url TEXT,
                stock INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
            """
        ]
        
        # Execute each query
        for query in queries:
            self.supabase.table('categories').select('*').execute()  # This is just to test connection
            
        # Insert test data
        self.supabase.table('categories').upsert([
            {
                'name': 'Outillage a main',
                'slug': 'outillage-a-main',
                'description': 'Outils manuels pour bricolage'
            },
            {
                'name': 'Peinture',
                'slug': 'peinture',
                'description': 'Peintures et accessoires'
            }
        ]).execute()

        self.supabase.table('brands').upsert([
            {
                'name': 'Stanley',
                'slug': 'stanley',
                'description': 'Outillage professionnel'
            },
            {
                'name': 'Dulux Valentine',
                'slug': 'dulux-valentine',
                'description': 'Peintures de qualite'
            }
        ]).execute()

        return True
    except Exception as e:
        logging.error(f"Error initializing tables: {str(e)}")
        raise e