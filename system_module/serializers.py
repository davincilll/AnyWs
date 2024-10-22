from rest_framework import serializers

from system_module.models import SystemConfiguration


class SystemConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfiguration
        exclude = ('id',)
