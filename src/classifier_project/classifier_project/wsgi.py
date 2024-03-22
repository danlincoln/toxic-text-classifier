"""
WSGI config for classifier_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

from classifier_app.classifier import Classifier
from django.core.wsgi import get_wsgi_application
import logging
import os

logging.basicConfig(
    format="%(asctime)s [%(name)s] %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger("WSGI")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "classifier_project.settings")

Classifier().train_model()
application = get_wsgi_application()
logger.info("Site ready to serve: http://localhost:8000")
