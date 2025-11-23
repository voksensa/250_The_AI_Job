"""OpenTelemetry configuration for Prometheus metrics."""

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from prometheus_client import make_asgi_app

from ..settings import settings


def setup_telemetry(app_name: str = "agent-runtime"):
    """Configure OpenTelemetry with Prometheus exporter.

    Returns:
        ASGI app serving metrics at /metrics
    """
    # Resource metadata
    resource = Resource(attributes={
        SERVICE_NAME: app_name,
        "environment": settings.environment
    })

    # Prometheus Reader
    # This registers itself with the default prometheus_client registry
    reader = PrometheusMetricReader()
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

    # Create ASGI app for /metrics
    return make_asgi_app()

def get_meter(name: str):
    """Get a named meter."""
    return metrics.get_meter(name)
