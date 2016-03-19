"""
WSGI config for plantilla_serviciosbases_oracle project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unidaddiagnosticomolecular.settings.test")

application = get_wsgi_application()
