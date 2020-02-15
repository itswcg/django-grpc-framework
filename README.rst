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

::

    INSTALLED_APPS = [
        ...
        'grpc_framework',
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

