from django.apps import AppConfig


class SystemModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'system_module'
    verbose_name = "系统管理模块"


