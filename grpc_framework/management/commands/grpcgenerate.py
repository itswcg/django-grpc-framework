import sys

from django.core.management import BaseCommand
from grpc_framework.utils.tools import Generation
from grpc_framework.settings import grpc_settings


class Command(BaseCommand):
    help = "Generate server and client code"

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label', nargs='*',
            help='Specify the app label(s) to generate code for.',
        )

    def handle(self, *app_labels, **options):
        app_labels = set(app_labels)
        has_bad_labels = False
        for app_label in app_labels:
            if app_label not in grpc_settings.grpc_apps:
                self.stderr.write(f'Note: {app_label} is not in GRPC_APPS.')
                has_bad_labels = True
        if has_bad_labels:
            sys.exit(2)

        app_labels = grpc_settings.grpc_apps if not app_labels else app_labels

        for app_label in app_labels:
            gen = Generation(app_label)
            try:
                gen.run()
            except Exception as e:
                self.stderr.write(e)
            else:
                self.stdout.write(f'GRPC_APP: {app_label} generate success.')
