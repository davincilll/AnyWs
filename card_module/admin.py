from django.contrib import admin

from app.common.decorator.AdminDecorator import custom_admin_decorator
from card_module.models.WordCard import WordCard


# Register your models here.
@custom_admin_decorator(register_model=WordCard)
class WordCardAdmin(admin.ModelAdmin):
    pass