# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action

from app.common.decorator.ViewSetDecorator import router_register
from app.common.exceptionbox.success_response import SuccessResponse
from app.routers import system_module_router
from system_module.models import SystemConfiguration
from system_module.serializers import SystemConfigurationSerializer


# @router_register(router=system_module_router)
# class SystemConfigurationViewSet(viewsets.GenericViewSet):
#     """
#     getConfig: 获取系统配置信息,无需jwt
#     """
#     serializer_class = SystemConfigurationSerializer
#     queryset = SystemConfiguration.objects.all()
#
#     @action(detail=False, methods=['get'])
#     def get_config(self, request, *args, **kwargs):
#         instance = SystemConfiguration.get_solo()
#         serializer = self.get_serializer(instance)
#         return SuccessResponse(serializer.data)
