import os

from environ import Env, NoValue, logger
from environ.compat import ImproperlyConfigured


class CustomEnvLoader(Env):
    """
    Purpose: Load env vars from env file -> os -> default -> ImproperlyConfigured exception """

    NOTSET = NoValue()
    OS_ENVIRON = os.environ

    def get_value(self, var, cast=None, default=NOTSET, parse_default=False):
        """Return value for given environment variable.

        :param str var:
            Name of variable.
        :param collections.abc.Callable or None cast:
            Type to cast return value as.
        :param default:
             If var not present in environ, return this instead.
        :param bool parse_default:
            Force to parse default.
        :returns: Value from environment or default (if set).
        :rtype: typing.IO[typing.Any]
        """

        logger.debug(
            "get '%s' casted as '%s' with default '%s'",
            var, cast, default)

        var_name = f'{self.prefix}{var}'
        if var_name in self.scheme:
            var_info = self.scheme[var_name]

            try:
                has_default = len(var_info) == 2
            except TypeError:
                has_default = False

            if has_default:
                if not cast:
                    cast = var_info[0]

                if default is self.NOTSET:
                    try:
                        default = var_info[1]
                    except IndexError:
                        pass
            else:
                if not cast:
                    cast = var_info
        # two try except blocks because value may evaluate to false even if set already
        try:
            value = self.ENVIRON[var_name]
        except KeyError as exc:
            try:
                value = self.OS_ENVIRON[var_name]
            except KeyError as exc:
                if default is self.NOTSET:
                    error_msg = f'Set the {var} environment variable'
                    raise ImproperlyConfigured(error_msg) from exc

                value = default

        # Resolve any proxied values
        prefix = b'$' if isinstance(value, bytes) else '$'
        escape = rb'\$' if isinstance(value, bytes) else r'\$'
        if hasattr(value, 'startswith') and value.startswith(prefix):
            value = value.lstrip(prefix)
            value = self.get_value(value, cast=cast, default=default)

        if self.escape_proxy and hasattr(value, 'replace'):
            value = value.replace(escape, prefix)

        # Smart casting
        if self.smart_cast:
            if cast is None and default is not None and \
                    not isinstance(default, NoValue):
                cast = type(default)

        value = None if default is None and value == '' else value

        if value != default or (parse_default and value is not None):
            value = self.parse_value(value, cast)

        return value
