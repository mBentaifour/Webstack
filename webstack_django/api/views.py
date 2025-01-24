from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from ..supabase.client import get_supabase_client

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        supabase = get_supabase_client()
        response = supabase.table('products').select('*').execute()
        return [Product(**item) for item in response.data]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        supabase = get_supabase_client()
        user_id = self.request.user.id
        response = supabase.table('orders').select('*').eq('user_id', user_id).execute()
        return [Order(**item) for item in response.data]

    def perform_create(self, serializer):
        supabase = get_supabase_client()
        user_id = self.request.user.id
        data = {**serializer.validated_data, 'user_id': user_id}
        response = supabase.table('orders').insert(data).execute()
        return response.data[0]
