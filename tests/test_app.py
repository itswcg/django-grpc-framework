from django.test import TestCase

from grpc_framework.apps import GrpcFrameworkConfig


class TestApp(TestCase):
    def test_app_name(self):
        self.assertEqual(GrpcFrameworkConfig.name, 'grpc_framework')
