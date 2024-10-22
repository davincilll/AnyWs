from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status

from app.common.decorator.ViewSetDecorator import router_register
from app.common.exceptionbox.success_response import SuccessResponse
from app.routers import user_module_router
from user_module.serializers.UserModelSerializer import UserModelSerializer


@router_register(user_module_router)
class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        这里进行注册
        """
        # todo:完成邮箱验证注册逻辑
        pass


@router_register(user_module_router)
class UserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):  # noqa
        serializer = UserModelSerializer(request.user)
        return SuccessResponse(serializer.data, status_code=status.HTTP_200_OK)
