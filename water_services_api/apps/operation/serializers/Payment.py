from rest_framework import serializers

from water_services_api.apps.configuration.serializers.PaymentMethod import PaymentMethodSerializer
from water_services_api.apps.operation.models.Payment import Payment, PaymentDetail
from water_services_api.apps.operation.serializers.Client import ClientBasicSerializer
from water_services_api.apps.operation.serializers.Plan import PlanBasicSerializer


class PaymentSerializer(serializers.ModelSerializer):
    client = ClientBasicSerializer(many=False, read_only=True)
    plan = PlanBasicSerializer(many=False, read_only=True)
    payment_method = PaymentMethodSerializer(many=False, read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id', 'client', 'client_id', 'date', 'plan', 'plan_id', 'payment_method', 'payment_method_id',
            'serie_payment', 'nro_payment', 'nro_operation', 'total', 'user', 'is_active')


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