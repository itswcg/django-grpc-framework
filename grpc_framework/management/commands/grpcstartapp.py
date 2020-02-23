import os

import grpc_framework
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = "Creates a Django grpc app"
    missing_args_message = "You must provide an application name."

    def handle(self, **options):
        app_name = options.pop('name')
        target = options.pop('directory')
        super().handle('app', app_name, target, **options)

    def handle_template(self, template, subdir):
        template = os.path.join(grpc_framework.__path__[0], 'grpc_app_template')
        return template
