import sys

from django.conf import settings
from django.core.management.commands import runserver


class Command(runserver.Command):
    def on_bind(self, server_port):
        """modified command for verbose output
        and clear difference b/w prod and dev env settings"""
        quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"

        if self._raw_ipv6:
            addr = f"[{self.addr}]"
        elif self.addr == "0":
            addr = "0.0.0.0"
        else:
            addr = self.addr

        default_db = settings.DATABASES.get('default') # update the db here
        engine = default_db[
            "ENGINE"] if default_db else "set up the db in runserver command in apps/auth_/management/commands/runserver.py"

        database_type = "PRODUCTION" if settings.USE_PROD_DATABASE else "LOCAL"
        output = (
            f"**** Using {database_type} DATABASE ****\n"
            f"** ENGINE: {engine} **\n"
            f"Settings: {settings.SETTINGS_MODULE!r}\n"
            f"Dev server running at {self.protocol}://{addr}:{server_port}/\n"
            f"Storage static url : {settings.STATIC_URL}"
            f"Quit the server with {quit_command}."
        )

        print(output)
