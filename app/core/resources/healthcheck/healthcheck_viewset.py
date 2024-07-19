from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class HealthCheckViewSet(viewsets.GenericViewSet):

    permission_classes = [AllowAny]

    def list(self, request):
        return Response()

    @action(url_path='version', methods=['get'], detail=False)
    def get_version(self, request):
        return Response({
            'api_version': settings.API_VERSION,
        })
