from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'API Django avec Supabase',
        'endpoints': {
            'products': reverse('product-list', request=request),
            'orders': reverse('order-list', request=request),
        }
    })
