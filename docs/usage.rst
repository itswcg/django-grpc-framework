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

Signals
---------
Grpc_framework provides signals:

* grpc_framework.signals.grpc_server_init
* grpc_framework.signals.grpc_server_started
* grpc_framework.signals.grpc_server_shutdown
* grpc_framework.signals.grpc_request_started
* grpc_framework.signals.grpc_request_exception
* grpc_framework.signals.grpc_request_finished

Logs
-------
Grpc_framework provides default log interceptor, you can set your own LOGGING::

    [2020-02-24 07:29:06,271] /RouteGuide/RouteChat success 0

Important
----------
You can't rename any files by executing this command::

    python manage.py grpcstartapp <app_name>
