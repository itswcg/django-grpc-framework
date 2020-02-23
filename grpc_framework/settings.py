"""
Settings for gRPC framework are namespaced in the GRPC_FRAMEWORK setting.
For example your project's `settings` file might look like this:

GRPC_FRAMEWORK = {
    'INTERCEPTORS': [
       ('grpc_framework.interceptors.log.LoggerInterceptor', {}),
    ]
}

This module provides the `grpc_setting` object.
"""
from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

DEFAULTS = {
    # Interceptors
    'INTERCEPTORS': [
        ('grpc_framework.interceptors.log.LoggerInterceptor', {}),
    ]
}

IMPORT_STRINGS = [
    'INTERCEPTORS',
]


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [(import_from_string(item[0], setting_name), item[1]) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for GRPC setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class GrpcSettings:
    """
    A settings objects, that allows GRPC settings to be accessed as properties.
    """

    def __init__(self, defaults=None, import_strings=None):
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def grpc_apps(self):
        return getattr(settings, 'GRPC_APPS', [])

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'GRPC_FRAMEWORK', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


grpc_settings = GrpcSettings()


def reload_grpc_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'GRPC_FRAMEWORK':
        grpc_settings.reload()


setting_changed.connect(reload_grpc_settings)
