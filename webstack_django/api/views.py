from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from supabase import create_client

class ProductViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        response = supabase.table('products').select('*').execute()
        return Response(response.data)

    def retrieve(self, request, pk=None):
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        response = supabase.table('products').select('*').eq('id', pk).execute()
        if not response.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(response.data[0])

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        user_id = request.user.id
        response = supabase.table('orders').select('*').eq('user_id', user_id).execute()
        return Response(response.data)

    def create(self, request):
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        user_id = request.user.id
        data = {**request.data, 'user_id': user_id}
        response = supabase.table('orders').insert(data).execute()
        return Response(response.data[0], status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        user_id = request.user.id
        response = supabase.table('orders').select('*').eq('id', pk).eq('user_id', user_id).execute()
        if not response.data:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(response.data[0])
