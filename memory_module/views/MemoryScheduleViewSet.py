from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.common.decorator.ViewSetDecorator import router_register, params_check
from app.common.exceptionbox.success_response import SuccessResponse
from app.common.mixins.UserFilterMixin import UserFilterListRetrieveMixin
from app.routers import memory_module_router
from memory_module.models import MemorySchedule
from memory_module.serializers.MemoryScheduleModelSerializer import MemoryScheduleModelSerializer


@router_register(memory_module_router)
class MemoryScheduleViewSet(UserFilterListRetrieveMixin, GenericViewSet):
    """
    list: 需要jwt，获取所有的用户的MemorySchedule资源对象
    no_need_review: 需要jwt，只需要传入id参数即可，将MemorySchedule对象的设为不需要复习
    upgrade: 需要jwt，只需要传入id参数即可，将MemorySchedule对象的记忆阶段提升
    forget: 需要jwt，只需要传入id参数即可，将MemorySchedule对象记忆阶段重置
    learn: 需要jwt，只需要传入id参数即可，将MemorySchedule对象的记忆阶段设置为已学习
    """
    queryset = MemorySchedule.objects.all()
    serializer_class = MemoryScheduleModelSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated]
    pagination_class = None

    @params_check(required_params=['word_card_id'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def no_need_review(self, request):
        self.get_object().no_need_review()
        return SuccessResponse()

    @action(detail=True, methods=['post'])
    def upgrade(self, request):
        self.get_object().upgrade()
        return SuccessResponse()

    @action(detail=True, methods=['post'])
    def forget(self, request):
        self.get_object().forget()
        return SuccessResponse()
    @action(detail=True, methods=['post'])
    def learn(self, request):
        self.get_object().learn()
        return SuccessResponse()
