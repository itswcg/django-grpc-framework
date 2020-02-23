from django.test import TestCase

from grpc_framework.utils import credentials


class TestUtils(TestCase):
    def test_load_credential_from_args(self):
        args = 'test.crt,test.key'
        with self.assertRaises(FileNotFoundError):
            credentials.load_credential_from_args(args)
