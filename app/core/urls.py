from rest_framework.routers import SimpleRouter

from .resources.healthcheck.healthcheck_viewset import HealthCheckViewSet

base_router = SimpleRouter()
base_router.register(r"v1/health-check", HealthCheckViewSet, basename="health-check")

urlpatterns = base_router.urls
