import importlib

from django.apps import AppConfig


class UserModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_module'
    verbose_name = "用户管理模块"
    def ready(self):
        importlib.import_module('user_module.signals')
