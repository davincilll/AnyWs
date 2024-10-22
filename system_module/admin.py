from django.contrib import admin
from solo.admin import SingletonModelAdmin

from system_module.models import SystemConfiguration

admin.site.register(SystemConfiguration, SingletonModelAdmin)
