from rest_framework.serializers import ModelSerializer

from memory_module.models import MemorySchedule


class MemoryScheduleModelSerializer(ModelSerializer):
    class Meta:
        model = MemorySchedule
        fields = '__all__'
