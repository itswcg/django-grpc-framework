import os
import grpc_framework
from django.core.management.templates import TemplateCommand


class GrpcTemplateCommand(TemplateCommand):

    def handle_template(self, template, subdir):
        template = os.path.join(grpc_framework.__path__[0], 'grpc_app_template')
        return template
