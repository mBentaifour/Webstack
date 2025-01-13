import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from main.models.order import Order, Payment

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        handle_payment_intent_succeeded(payment_intent)
    elif event.type == 'payment_intent.payment_failed':
        payment_intent = event.data.object
        handle_payment_intent_failed(payment_intent)
    elif event.type == 'charge.refunded':
        charge = event.data.object
        handle_refund_succeeded(charge)
    elif event.type == 'charge.refund.updated':
        refund = event.data.object
        handle_refund_updated(refund)

    return HttpResponse(status=200)

def handle_payment_intent_succeeded(payment_intent):
    """Gère un paiement réussi"""
    try:
        payment = Payment.objects.get(transaction_id=payment_intent.id)
        order = payment.order

        # Mettre à jour le statut du paiement
        payment.status = 'completed'
        payment.save()

        # Mettre à jour le statut de la commande
        order.status = 'paid'
        order.save()

        # Mettre à jour l'inventaire
        for item in order.items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()

    except Payment.DoesNotExist:
        # Log l'erreur ou gérer le cas où le paiement n'est pas trouvé
        pass

def handle_payment_intent_failed(payment_intent):
    """Gère un paiement échoué"""
    try:
        payment = Payment.objects.get(transaction_id=payment_intent.id)
        
        # Mettre à jour le statut du paiement
        payment.status = 'failed'
        payment.error_message = payment_intent.last_payment_error.message if payment_intent.last_payment_error else 'Payment failed'
        payment.save()

        # Mettre à jour le statut de la commande
        order = payment.order
        order.status = 'payment_failed'
        order.save()

    except Payment.DoesNotExist:
        pass

def handle_refund_succeeded(charge):
    """Gère un remboursement réussi"""
    try:
        payment = Payment.objects.get(transaction_id=charge.payment_intent)
        
        # Mettre à jour le statut du paiement
        payment.status = 'refunded'
        payment.save()

        # Mettre à jour le statut de la commande
        order = payment.order
        order.status = 'refunded'
        order.save()

        # Remettre à jour l'inventaire
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

    except Payment.DoesNotExist:
        pass

def handle_refund_updated(refund):
    """Gère une mise à jour de remboursement"""
    try:
        payment = Payment.objects.get(transaction_id=refund.payment_intent)
        
        if refund.status == 'failed':
            # Le remboursement a échoué, remettre les statuts à 'completed'
            payment.status = 'completed'
            payment.save()

            order = payment.order
            order.status = 'paid'
            order.save()

    except Payment.DoesNotExist:
        pass
