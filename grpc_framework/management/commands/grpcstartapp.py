from grpc_framework.templates import GrpcTemplateCommand


class Command(GrpcTemplateCommand):
    help = "Creates a Django grpc app"
    missing_args_message = "You must provide an application name."

    def handle(self, **options):
        app_name = options.pop('name')
        target = options.pop('directory')
        super().handle('app', app_name, target, **options)
