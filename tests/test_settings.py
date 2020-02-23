from django.test import TestCase

from grpc_framework.settings import GrpcSettings, grpc_settings


class TestSettings(TestCase):
    def test_import_error_message_maintained(self):
        """
        Make sure import errors are captured and raised sensibly.
        """
        settings = GrpcSettings({
            'INTERCEPTORS': [
                ('tests.invalid_module.InvalidClassName', {})
            ]
        })
        with self.assertRaises(ImportError):
            _ = settings.INTERCEPTORS

    def test_grpc_app(self):
        """
        Mare sure grpc_apps is a list.
        """
        self.assertTrue(isinstance(grpc_settings.grpc_apps, list))
