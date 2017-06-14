"""
WSGI config for danjaysci project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os, sys
sys.path.append("/var/www/danjaysci.com/danjaysci/")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "danjaysci.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
