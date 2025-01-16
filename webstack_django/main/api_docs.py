from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

# Common response schemas
ERROR_RESPONSES = {
    400: {"description": "Bad Request"},
    401: {"description": "Unauthorized"},
    403: {"description": "Forbidden"},
    404: {"description": "Not Found"},
    500: {"description": "Internal Server Error"},
}

# Common parameters
PAGINATION_PARAMETERS = [
    OpenApiParameter(
        name="page",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="Page number",
        default=1,
    ),
    OpenApiParameter(
        name="page_size",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="Number of items per page",
        default=10,
    ),
]

# Authentication decorator
def auth_schema(tags=None, responses=None):
    """
    Decorator to add authentication and common responses to API endpoints
    """
    if responses is None:
        responses = {}
    
    responses.update(ERROR_RESPONSES)
    
    def wrapper(view_func):
        return extend_schema(
            tags=tags,
            responses=responses,
            security=[{"Bearer": []}],
        )(view_func)
    return wrapper

# Example view extension
class OrderViewExtension(OpenApiViewExtension):
    target_class = 'main.views.order_views.OrderViewSet'

    def view_replacement(self):
        from main.serializers.order import OrderSerializer
        
        class Extended(self.target_class):
            @extend_schema(
                summary="Create a new order",
                description="Creates a new order with the provided details",
                request=OrderSerializer,
                responses={201: OrderSerializer},
                tags=['Orders'],
            )
            def create(self, request, *args, **kwargs):
                return super().create(request, *args, **kwargs)
                
        return Extended
