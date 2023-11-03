from rest_framework import serializers

from water_services_api.apps.operation.models.Payment import Payment, PaymentDetail
from water_services_api.apps.operation.serializers.Client import ClientBasicSerializer


class PaymentSerializer(serializers.ModelSerializer):
    client = ClientBasicSerializer(many=False, read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id', 'client', 'client_id', 'date', 'plan_id', 'payment_method_id', 'serie_payment', 'nro_payment', 'nro_operation',
            'total', 'user', 'is_active')


class PaymentBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'serie_payment', 'nro_payment',)


class PaymentItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = ('id', 'payment', 'service', 'quantity', 'cost', 'amount')


class PaymentItemsBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = ('ser', 'service', 'cost', 'amount')