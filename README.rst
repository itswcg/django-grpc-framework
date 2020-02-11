=============================
django-grpc-framework
=============================

.. image:: https://badge.fury.io/py/django-grpc-framework.svg
    :target: https://badge.fury.io/py/django-grpc-framework

.. image:: https://travis-ci.org/itswcg/django-grpc-framework.svg?branch=master
    :target: https://travis-ci.org/itswcg/django-grpc-framework

.. image:: https://codecov.io/gh/itswcg/django-grpc-framework/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/itswcg/django-grpc-framework

gRPC for Django

Documentation
-------------

The full documentation is at https://django-grpc-framework.readthedocs.io.

Quickstart
----------

Install django-grpc-framework::

    pip install django-grpc-framework

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
