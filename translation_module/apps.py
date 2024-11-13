from django.apps import AppConfig


class TranslationModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translation_module'
    verbose_name = "翻译模块"
