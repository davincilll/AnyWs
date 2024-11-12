from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.common.decorator.ViewSetDecorator import router_register, params_check
from app.common.mixins.CustomCreateModelMixin import CustomCreateModelMixin
from app.common.mixins.PartialUpdateModelMixin import PartialUpdateModelMixin
from app.common.mixins.UserFilterMixin import UserFilterListRetrieveMixin
from app.routers import user_module_router
from user_module.models import UserProfile
from user_module.serializers.UserModelSerializer import UserProfileModelSerializer


@router_register(user_module_router)
class UserProfileViewSet(UserFilterListRetrieveMixin, GenericViewSet, PartialUpdateModelMixin,
                         CustomCreateModelMixin):
    """
    list: 需要jwt，获取所有的用户的UserProfile资源对象
    create: 需要jwt，创建用户的UserProfile资源对象，传入user参数是被禁止的，会自动从会话中获取user对象
    partial_update: 需要jwt，部分更新用户的UserProfile资源对象，传入user参数是被禁止的，会自动从会话中获取user对象，允许更新的字段包括TODO
    destroy: 需要jwt，删除用户的UserProfile资源对象
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated]

    @params_check(not_allowed_params=["user"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
