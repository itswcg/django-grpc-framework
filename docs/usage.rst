=====
Usage
=====

Interceptors
-----------------
Add interceptor to GRPC_FRAMEWORK like this:
::

    GRPC_FRAMEWORK = {
        'INTERCEPTORS': [
            ('grpc_framework.interceptors.log.LoggerInterceptor', {}),
        ]
    }

Grpc_framework provides log and header interceptor, you can define it yourself, then add it.

Credentials
--------------
You can start a ssl server by command::

    python manage.py runserver --certificate_chain_pairs=server.crt,server.key

Important
----------
You can't rename any files by executing this command::

    python manage.py grpcstartapp <app_name>
