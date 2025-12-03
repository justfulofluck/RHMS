from rest_framework import serializers
from .models import Patient, Notification

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Patient
        fields = '__all__'

class PatientProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    name = serializers.CharField(source='user.first_name')

    class Meta:
        model = Patient
        fields = ['id', 'name', 'email', 'age', 'gender', 'phone', 'address', 'photo', 'medical_history']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        name = user_data.get('first_name')
        
        if name:
            instance.user.first_name = name
            instance.user.save()

        return super().update(instance, validated_data)

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at']
        read_only_fields = ['created_at']
