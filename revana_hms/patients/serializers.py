from rest_framework import serializers
from .models import Patient, Notification

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Patient
        fields = '__all__'

class PatientProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    # name is now a field on Patient model, so no source needed
    # Aliases for Mobile App Compatibility
    full_name = serializers.CharField(source='name', required=False)
    phone_number = serializers.CharField(source='phone', required=False)

    class Meta:
        model = Patient
        fields = ['id', 'name', 'full_name', 'email', 'age', 'gender', 'phone', 'phone_number', 'address', 'photo', 'medical_history']

    def update(self, instance, validated_data):
        # We don't need to pop 'user' since we are not updating User model for name anymore
        # but just in case we need to handle other user fields later, we can keep the pattern
        # For now, standard update is sufficient for Patient fields (including name)
        return super().update(instance, validated_data)

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at']
        read_only_fields = ['created_at']
