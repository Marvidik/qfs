from rest_framework import serializers
from .models import Deposit, Withdraw


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'user', 'amount', 'currency', 'transaction_id', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'transaction_id', 'created_at', 'user']


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = ['id', 'user', 'amount', 'currency', 'wallet_address', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at', 'user']
