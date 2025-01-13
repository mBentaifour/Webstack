from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from supabase import create_client
import os
from dotenv import load_dotenv
from .authentication import SupabaseAuthentication
import logging

# Charger les variables d'environnement
load_dotenv()

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ViewSet):
    """
    ViewSet pour gérer les produits via Supabase
    """
    authentication_classes = [SupabaseAuthentication]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_anon_key = os.getenv('SUPABASE_ANON_KEY')
        self.supabase_service_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not self.supabase_url or not self.supabase_anon_key or not self.supabase_service_key:
            raise Exception("Les variables d'environnement Supabase sont requises")
        
        # Client pour les opérations de lecture
        self.read_client = create_client(self.supabase_url, self.supabase_anon_key)
        # Client pour les opérations d'écriture
        self.write_client = create_client(self.supabase_url, self.supabase_service_key)
        
    def get_permissions(self):
        """
        Définir les permissions en fonction de l'action
        """
        if self.action in ['list', 'retrieve', 'search']:
            permission_classes = []
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        """Récupérer tous les produits"""
        try:
            response = self.read_client.table('products').select("*").execute()
            return Response(response.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """Créer un nouveau produit"""
        try:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
                
            response = self.write_client.table('products').insert(request.data).execute()
            return Response(response.data[0], status=status.HTTP_201_CREATED)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Récupérer un produit spécifique"""
        try:
            response = self.read_client.table('products').select("*").eq('id', pk).execute()
            if response.data:
                return Response(response.data[0])
            return Response({"error": "Produit non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Mettre à jour un produit"""
        try:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
                
            response = self.write_client.table('products').update(request.data).eq('id', pk).execute()
            if response.data:
                return Response(response.data[0])
            return Response({"error": "Produit non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Supprimer un produit"""
        try:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            
            if not request.user.is_staff:
                raise PermissionDenied('Permission refusée - Accès admin requis')
                
            response = self.write_client.table('products').delete().eq('id', pk).execute()
            if response.data:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Produit non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def search(self, request):
        """Rechercher des produits"""
        try:
            search_term = request.data.get('search', '').lower()
            response = self.read_client.table('products').select("*").ilike('name', f"%{search_term}%").execute()
            return Response(response.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_products(request):
    """Récupère la liste des produits"""
    try:
        adapter = SupabaseAdapter()
        products = adapter.get_products()
        return Response(products, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des produits: {str(e)}")
        return Response(
            {"error": "Erreur lors de la récupération des produits"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_product_details(request, product_id):
    """Récupère les détails d'un produit"""
    try:
        adapter = SupabaseAdapter()
        product = adapter.get_product_by_id(product_id)
        if product:
            return Response(product, status=status.HTTP_200_OK)
        return Response(
            {"error": "Produit non trouvé"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du produit: {str(e)}")
        return Response(
            {"error": "Erreur lors de la récupération du produit"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    """Crée un nouveau produit"""
    try:
        adapter = SupabaseAdapter()
        product_data = request.data
        product = adapter.create_product(product_data)
        return Response(product, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Erreur lors de la création du produit: {str(e)}")
        return Response(
            {"error": "Erreur lors de la création du produit"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
