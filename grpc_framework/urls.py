from django.conf.urls import url
from django.views.generic import TemplateView

app_name = 'grpc_framework'
urlpatterns = [
    url(r'', TemplateView.as_view(template_name="base.html")),
]
