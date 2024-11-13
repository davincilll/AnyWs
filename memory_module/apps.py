import importlib

from django.apps import AppConfig


class MemoryModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'memory_module'
    verbose_name = '记忆模块'
    def ready(self):
        importlib.import_module('memory_module.signals')
