from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal
from ..services.transaction_service import TransactionService
from ..serializers.transaction_serializer import TransactionSerializer

transaction_service = TransactionService()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    """Crée une nouvelle transaction"""
    try:
        amount = Decimal(request.data.get('amount'))
        payment_method = request.data.get('payment_method')
        billing_info = {
            'name': request.data.get('billing_name'),
            'address': request.data.get('billing_address'),
            'city': request.data.get('billing_city'),
            'country': request.data.get('billing_country'),
            'postal_code': request.data.get('billing_postal_code')
        }
        
        transaction = transaction_service.create_transaction(
            user_id=request.user.id,
            amount=amount,
            payment_method=payment_method,
            billing_info=billing_info
        )
        
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_payment(request, transaction_id):
    """Traite le paiement d'une transaction"""
    try:
        transaction = transaction_service.get_transaction_details(transaction_id)
        if not transaction:
            return Response(
                {'error': 'Transaction non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        if transaction.user_id != request.user.id:
            return Response(
                {'error': 'Non autorisé'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        payment_details = request.data.get('payment_details', {})
        success = transaction_service.process_payment(transaction, payment_details)
        
        if success:
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Le paiement a échoué'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    """Récupère l'historique des transactions de l'utilisateur"""
    try:
        transactions = transaction_service.get_transaction_history(request.user.id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_details(request, transaction_id):
    """Récupère les détails d'une transaction spécifique"""
    try:
        transaction = transaction_service.get_transaction_details(transaction_id)
        
        if not transaction:
            return Response(
                {'error': 'Transaction non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        if transaction.user_id != request.user.id:
            return Response(
                {'error': 'Non autorisé'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
