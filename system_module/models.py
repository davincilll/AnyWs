
from django.db import models
from solo.models import SingletonModel





class SystemConfiguration(SingletonModel):
    # 默认配置
    demo_config = models.CharField(max_length=255, default='', verbose_name='默认配置')
    def __str__(self):
        return "系统配置"

    class Meta:
        db_table = 'system_configuration'
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name
