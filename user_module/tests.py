# Create your tests here.
import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()
from card_module.serializers.WordCardModelSerializer import WordCardModelSerializer


from drf_jsonschema_serializer import to_jsonschema

from rest_framework import serializers




# print(json_schema)

