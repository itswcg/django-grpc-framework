import errno
import os
import re
import sys
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import autoreload

from grpc_framework.server import GrpcServer
from grpc_framework.utils.credentials import load_credential_from_file, load_credential_from_args

naiveip_re = re.compile(r"""^(?:
(?P<addr>
    (?P<ipv4>\d{1,3}(?:\.\d{1,3}){3}) |         # IPv4 address
    (?P<ipv6>\[[a-fA-F0-9:]+\]) |               # IPv6 address
    (?P<fqdn>[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*) # FQDN
):)?(?P<port>\d+)$""", re.X)


class Command(BaseCommand):
    help = "Starts a GRPC server"

    requires_system_checks = False
    stealth_options = ('shutdown_message',)

    default_addr = '0.0.0.0'
    default_port = '50051'
    protocol = 'grpc'
    server_cls = GrpcServer

    def add_arguments(self, parser):
        parser.add_argument(
            'addrport', nargs='?',
            help='Optional port number, or ipaddr:port'
        )

        parser.add_argument(
            '--workers', dest='max_workers',
            help='Number of maximum worker threads'
        )

        parser.add_argument(
            '--noreload', action='store_false', dest='use_reloader',
            help='Tells Django to NOT use the auto-reloader.',
        )

        parser.add_argument(
            '--certificate_chain_pairs', dest='certificate_chain_pairs',
            help='Private_key_certificate_chain_pairs'
        )

        parser.add_argument(
            '--root_certificates', dest='root_certificates',
            help=''
        )

    def handle(self, *args, **options):
        if not options['addrport']:
            self.addr = ''
            self.port = self.default_port
        else:
            m = re.match(naiveip_re, options['addrport'])
            if m is None:
                raise CommandError('"%s" is not a valid port number '
                                   'or address:port pair.' % options['addrport'])
            self.addr, _ipv4, _ipv6, _fqdn, self.port = m.groups()
            if not self.port.isdigit():
                raise CommandError("%r is not a valid port number." % self.port)
        if not self.addr:
            self.addr = self.default_addr
        self.run(**options)

    def run(self, **options):
        """Run the server, using the autoreloader if needed."""
        use_reloader = options['use_reloader']

        if use_reloader:
            try:
                autoreload.run_with_reloader(self.inner_run, **options)
            except AttributeError:
                self.inner_run(None, **options)
        else:
            self.inner_run(None, **options)

    def inner_run(self, *args, **options):
        # If an exception was silenced in ManagementUtility.execute in order
        # to be raised in the child process, raise it now.
        autoreload.raise_last_exception()
        max_workers = options.get('max_workers', 5)

        # Handle certificate
        ssl, server_kwargs = False, {}
        certificate_chain_pairs = options.get('certificate_chain_pairs', '')
        root_certificates = options.get('root_certificates', '')

        if certificate_chain_pairs:
            ssl = True
            certificate_chain_pairs = load_credential_from_args(certificate_chain_pairs)
            if root_certificates:
                root_certificates = load_credential_from_file(root_certificates)
                server_kwargs['root_certificate'] = root_certificates
            server_kwargs['certificate_key'] = certificate_chain_pairs[0]
            server_kwargs['certificate'] = certificate_chain_pairs[1]

        # 'shutdown_message' is a stealth option.
        shutdown_message = options.get('shutdown_message', '')
        quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'

        self.stdout.write("Performing system checks...\n\n")
        self.check(display_num_errors=True)
        # Need to check migrations here, so can't use the
        # requires_migrations_check attribute.
        self.check_migrations()
        now = datetime.now().strftime('%B %d, %Y - %X')
        self.stdout.write(now)
        self.stdout.write((
                              "Django version %(version)s, using settings %(settings)r\n"  # noqa
                              "Starting development server at %(protocol)s:%(addr)s:%(port)s\n"
                              "Quit the server with %(quit_command)s.\n"
                          ) % {
                              "version": self.get_version(),
                              "settings": settings.SETTINGS_MODULE,
                              "protocol": self.protocol,
                              "addr": '%s' % self.addr,
                              "port": self.port,
                              "quit_command": quit_command,
                          })

        try:
            server = self.server_cls(max_workers=max_workers, ssl=ssl)
            with server.start(self.addr, self.port, **server_kwargs) as ser:
                ser.wait_for_termination()
        except OSError as e:
            # Use helpful error messages instead of ugly tracebacks.
            ERRORS = {
                errno.EACCES: "You don't have permission to access that port.",
                errno.EADDRINUSE: "That port is already in use.",
                errno.EADDRNOTAVAIL: "That IP address can't be assigned to.",
            }
            try:
                error_text = ERRORS[e.errno]
            except KeyError:
                error_text = e
            self.stderr.write("Error: %s" % error_text)
            # Need to use an OS exit because sys.exit doesn't work in a thread
            os._exit(1)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)
