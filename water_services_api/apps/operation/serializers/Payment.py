from rest_framework import serializers

from water_services_api.apps.operation.models.Payment import Payment, PaymentDetail


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id', 'client', 'date', 'plan', 'payment_method', 'serie_payment', 'nro_payment', 'nro_operation',
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