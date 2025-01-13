import uuid
from decimal import Decimal
from typing import Dict, Optional
from django.db import transaction
from ..models.transaction import Transaction
from ..supabase_adapter import SupabaseAdapter

class TransactionService:
    def __init__(self):
        self.supabase = SupabaseAdapter()
    
    def create_transaction(self, user_id: str, amount: Decimal, payment_method: str,
                         billing_info: Dict) -> Transaction:
        """Crée une nouvelle transaction"""
        with transaction.atomic():
            # Générer un ID unique pour la transaction
            transaction_id = str(uuid.uuid4())
            
            # Créer la transaction dans la base de données
            new_transaction = Transaction.objects.create(
                transaction_id=transaction_id,
                user_id=user_id,
                amount=amount,
                payment_method=payment_method,
                billing_name=billing_info.get('name'),
                billing_address=billing_info.get('address'),
                billing_city=billing_info.get('city'),
                billing_country=billing_info.get('country'),
                billing_postal_code=billing_info.get('postal_code')
            )
            
            # Enregistrer dans Supabase
            self.supabase.create_transaction({
                'transaction_id': transaction_id,
                'user_id': user_id,
                'amount': float(amount),
                'status': Transaction.PENDING,
                'payment_method': payment_method
            })
            
            return new_transaction
    
    def process_payment(self, transaction: Transaction, payment_details: Dict) -> bool:
        """Traite le paiement d'une transaction"""
        try:
            # Ici, vous intégrerez votre logique de paiement (Stripe, PayPal, etc.)
            # Pour l'exemple, nous simulons un succès
            payment_successful = True
            
            if payment_successful:
                transaction.mark_as_completed()
                # Mettre à jour dans Supabase
                self.supabase.update_transaction_status(
                    transaction.transaction_id,
                    Transaction.COMPLETED
                )
                return True
            else:
                transaction.mark_as_failed()
                self.supabase.update_transaction_status(
                    transaction.transaction_id,
                    Transaction.FAILED
                )
                return False
                
        except Exception as e:
            transaction.mark_as_failed()
            self.supabase.update_transaction_status(
                transaction.transaction_id,
                Transaction.FAILED
            )
            raise e
    
    def get_transaction_history(self, user_id: str) -> list:
        """Récupère l'historique des transactions d'un utilisateur"""
        return Transaction.objects.filter(user_id=user_id).order_by('-created_at')
    
    def get_transaction_details(self, transaction_id: str) -> Optional[Transaction]:
        """Récupère les détails d'une transaction spécifique"""
        try:
            return Transaction.objects.get(transaction_id=transaction_id)
        except Transaction.DoesNotExist:
            return None
