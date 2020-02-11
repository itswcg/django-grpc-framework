=====
Usage
=====

To use django-grpc-framework in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'grpc_framework.apps.GrpcFrameworkConfig',
        ...
    )

Add django-grpc-framework's URL patterns:

.. code-block:: python

    from grpc_framework import urls as grpc_framework_urls


    urlpatterns = [
        ...
        url(r'^', include(grpc_framework_urls)),
        ...
    ]
