from rest_framework import serializers
from ..models.transaction import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'transaction_id',
            'amount',
            'status',
            'payment_method',
            'created_at',
            'updated_at',
            'billing_name',
            'billing_address',
            'billing_city',
            'billing_country',
            'billing_postal_code'
        ]
        read_only_fields = ['transaction_id', 'status', 'created_at', 'updated_at']
