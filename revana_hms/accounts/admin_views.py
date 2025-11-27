from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from accounts.models import User, HospitalAdminProfile
from doctors.models import Doctor
from accounts.serializers import UserSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_hospital_admins(request):
    hospital_admins = User.objects.filter(role='hospital_admin')
    serializer = UserSerializer(hospital_admins, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_doctors(request):
    doctors = User.objects.filter(role='doctor')
    serializer = UserSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
