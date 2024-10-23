from django.contrib import admin
from solo.admin import SingletonModelAdmin

from system_module.models import SystemConfiguration

admin.site.register(SystemConfiguration, SingletonModelAdmin)

# 设置管理后台的名称和标题
admin.site.site_header = 'AnyWs后台管理'
admin.site.site_title = 'AnyWs后台管理'
admin.site.index_title = 'AnyWs后台管理'
