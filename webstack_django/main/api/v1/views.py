from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models.order import Order, Payment
from .serializers import OrderSerializer, PaymentSerializer
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les commandes.
    
    retrieve:
    Retourne les détails d'une commande spécifique.

    list:
    Retourne la liste des commandes de l'utilisateur connecté.
    Les administrateurs peuvent voir toutes les commandes.

    create:
    Crée une nouvelle commande.
    Requiert une liste d'articles (items) avec les quantités.

    update:
    Met à jour une commande existante.
    Seuls certains champs peuvent être modifiés une fois la commande créée.

    partial_update:
    Met à jour partiellement une commande existante.

    delete:
    Supprime une commande (uniquement si elle n'est pas encore payée).
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        """
        Initie le processus de paiement pour une commande.
        
        Crée une intention de paiement Stripe et retourne le client_secret
        nécessaire pour finaliser le paiement côté client.
        
        Paramètres:
        - pk (int): ID de la commande
        
        Retourne:
        - client_secret: Clé secrète pour le paiement Stripe
        - payment_id: ID du paiement créé
        """
        order = self.get_object()
        
        try:
            # Créer une intention de paiement Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=int(order.total * 100),  # Stripe utilise les centimes
                currency='eur',
                metadata={'order_id': order.id}
            )

            # Créer un enregistrement de paiement
            payment = Payment.objects.create(
                order=order,
                amount=order.total,
                payment_method='card',
                transaction_id=payment_intent.id,
                payment_details={'client_secret': payment_intent.client_secret}
            )

            return Response({
                'client_secret': payment_intent.client_secret,
                'payment_id': payment.id
            })

        except stripe.error.StripeError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        """
        Confirme le paiement d'une commande.
        
        Vérifie le statut du paiement avec Stripe et met à jour
        le statut de la commande si le paiement est réussi.
        
        Paramètres:
        - pk (int): ID de la commande
        - payment_intent_id (str): ID de l'intention de paiement Stripe
        
        Retourne:
        - status: Statut de la confirmation ('payment_confirmed' ou erreur)
        """
        order = self.get_object()
        payment_intent_id = request.data.get('payment_intent_id')

        try:
            # Vérifier le paiement avec Stripe
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            if payment_intent.status == 'succeeded':
                # Mettre à jour la commande et le paiement
                order.status = 'paid'
                order.save()

                payment = order.payments.filter(transaction_id=payment_intent_id).first()
                if payment:
                    payment.status = 'completed'
                    payment.save()

                return Response({'status': 'payment_confirmed'})
            else:
                return Response({
                    'error': 'Payment not succeeded'
                }, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour gérer les paiements.
    
    retrieve:
    Retourne les détails d'un paiement spécifique.

    list:
    Retourne la liste des paiements de l'utilisateur connecté.
    Les administrateurs peuvent voir tous les paiements.

    create:
    Crée un nouveau paiement.
    Généralement créé automatiquement lors du processus de paiement d'une commande.

    update:
    Met à jour un paiement existant.
    Réservé aux administrateurs.

    partial_update:
    Met à jour partiellement un paiement existant.
    Réservé aux administrateurs.

    delete:
    Supprime un paiement.
    Réservé aux administrateurs.
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(order__user=user)

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """
        Effectue le remboursement d'un paiement.
        
        Crée un remboursement via Stripe et met à jour les statuts
        du paiement et de la commande associée.
        
        Paramètres:
        - pk (int): ID du paiement
        - reason (str): Raison du remboursement
        
        Retourne:
        - status: Statut du remboursement ('refunded')
        - refund_id: ID du remboursement Stripe
        """
        payment = self.get_object()
        reason = request.data.get('reason')

        try:
            # Effectuer le remboursement via Stripe
            refund = stripe.Refund.create(
                payment_intent=payment.transaction_id,
                reason=reason
            )

            # Mettre à jour le statut du paiement
            payment.status = 'refunded'
            payment.refund_reason = reason
            payment.save()

            # Mettre à jour le statut de la commande
            payment.order.status = 'refunded'
            payment.order.save()

            return Response({'status': 'refunded', 'refund_id': refund.id})

        except stripe.error.StripeError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
