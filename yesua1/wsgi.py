"""
WSGI config for CrowdPlatform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import django

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yesua1.settings")
#django.setup()
import yesua1.startup as startup
startup.run()
application = get_wsgi_application()
