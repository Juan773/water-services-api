from rest_framework import serializers

from water_services_api.apps.configuration.models.PaymentMethod import PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
