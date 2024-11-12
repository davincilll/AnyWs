from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.viewsets import GenericViewSet

from app.common.decorator.ViewSetDecorator import router_register, params_check
from app.common.exceptionbox.success_response import SuccessResponse
from app.routers import user_module_router
from user_module.exceptions import CaptchaError, UsernameAlreadyExistsError
from user_module.serializers.UserModelSerializer import UserModelSerializer


@api_view(['GET'])
@swagger_auto_schema(
    operation_description="获取验证码",
    responses={
        200: openapi.Response(
            description="成功获取验证码",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'captcha_key': openapi.Schema(type=openapi.TYPE_STRING, description='验证码键'),
                    'image_url': openapi.Schema(type=openapi.TYPE_STRING, description='验证码图像的 URL'),
                }
            )
        )
    }
)
def get_captcha(request):
    # 创建验证码
    captcha = CaptchaStore.generate_key()
    image_url = captcha_image_url(captcha)
    return SuccessResponse({'captcha_key': captcha, 'image_url': image_url})


# @api_view(['POST'])
# @swagger_auto_schema(
#     operation_description="发送邮箱验证码",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'email': openapi.Schema(type=openapi.TYPE_STRING, description='注册邮箱'),
#             'x_captcha_key': openapi.Schema(type=openapi.TYPE_STRING, description='验证码键'),
#             'x_captcha_result': openapi.Schema(type=openapi.TYPE_STRING, description='验证码结果'),
#         },
#         required=['email', 'x_captcha_key', 'x_captcha_result']
#     ),
# )
# @params_check(required_params=['email', 'x_captcha_key', 'x_captcha_result'])
# def send_register_verification_code(request):
#     """
#     发送邮箱验证码
#     """
#     # 验证验证码
#     captcha_key = request.data['x_captcha_key']
#     result = request.data['x_captcha_result']
#     if not CaptchaStore.objects.filter(hashkey=captcha_key, response=result).exists():
#         raise CaptchaError()
#     # 检验邮箱是否存在
#     email = request.data['email'].lower()
#     # 查询邮箱是否被注册过
#     if User.objects.filter(email=email).exists():
#         raise EmailAlreadyExistsError()
#     # 发送邮件
#     subject = "AnyWs"
#     rand_str = send_message(email, subject)
#     # 将验证码放入缓存，有效时间是10min
#     cache.set(email, rand_str, 600)
#     return SuccessResponse()


@api_view(['POST'])
@swagger_auto_schema(
    operation_description="用户注册",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
            'x_captcha_key': openapi.Schema(type=openapi.TYPE_STRING, description='验证码键'),
            'x_captcha_result': openapi.Schema(type=openapi.TYPE_STRING, description='验证码结果'),
        },
        required=['username', 'password', 'x_captcha_key', 'x_captcha_result']
    )
)
@params_check(required_params=['x_captcha_key', 'x_captcha_result', 'username', 'password'])
def register(request):
    """
    这里进行注册
    """
    # # 获取注册邮箱
    # email = request.data['email'].lower()
    # # 获取邮箱验证码
    # code = request.data['verification_code']
    # 获取用户名
    username = request.data['username']
    # 获取密码
    password = request.data['password']
    captcha_key = request.data['x_captcha_key']
    result = request.data['x_captcha_result']
    # 查询邮箱是否被注册过
    if User.objects.filter(username=username).exists():
        return UsernameAlreadyExistsError()
    # 使用session的方式保持登录
    if not CaptchaStore.objects.filter(hashkey=captcha_key, response=result).exists():
        raise CaptchaError()
    User.objects.create_user(
        username=username,
        password=password
    )
    return SuccessResponse()


# @api_view(['POST'])
# @swagger_auto_schema(
#     operation_description="发送邮箱验证码",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'email': openapi.Schema(type=openapi.TYPE_STRING, description='注册邮箱'),
#             'x_captcha_key': openapi.Schema(type=openapi.TYPE_STRING, description='验证码键'),
#             'x_captcha_result': openapi.Schema(type=openapi.TYPE_STRING, description='验证码结果'),
#         },
#         required=['email', 'x_captcha_key', 'x_captcha_result']
#     ),
# )
# @params_check(required_params=['email', 'x_captcha_key', 'x_captcha_result'])
# def send_modify_pwd_verification_code(request):
#     # 验证验证码
#     captcha_key = request.data['x_captcha_key']
#     result = request.data['x_captcha_result']
#     if not CaptchaStore.objects.filter(hashkey=captcha_key, response=result).exists():
#         raise CaptchaError()
#     # 检验邮箱是否存在
#     email = request.data['email'].lower()
#     # 查询邮箱是否被注册过
#     if not User.objects.filter(email=email).exists():
#         raise EmailNotExistsError()
#     # 发送邮件
#     subject = "AnyWs"
#     rand_str = send_message(email, subject)
#     # 将验证码放入缓存，有效时间是10min
#     cache.set(email, rand_str, 600)
#     return SuccessResponse()

# @api_view(['POST'])
# @swagger_auto_schema(
#     operation_summary='修改密码',
#     operation_description='使用邮箱和验证码来修改用户密码',
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'email': openapi.Schema(type=openapi.TYPE_STRING, description='用户注册的邮箱'),
#             'verification_code': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱验证码'),
#             'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='新密码'),
#         },
#         required=['email', 'verification_code', 'new_password'],
#     ))
# @params_check(required_params=['email', 'verification_code', 'new_password'])
# def modify_pwd(request):
#     """
#     修改密码
#     """
#     # 获取注册邮箱
#     email = request.data['email'].lower()
#     # 获取邮箱验证码
#     code = request.data['verification_code']
#     # 获取新密码
#     new_password = request.data['new_password']
#     # 查询邮箱是否被注册过
#     user = User.objects.filter(email=email).get()
#     if not user:
#         return EmailNotExistsError()
#     # 使用session的方式保持登录
#     if cache.get(email) == code:  # 验证验证
#         user.set_password(new_password)
#         user.save()
#         return SuccessResponse()
#     else:
#         raise VerificationCodeError()


@router_register(user_module_router)
class UserViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserModelSerializer
    pagination_class = None

    def list(self, request):  # noqa
        serializer = UserModelSerializer(request.user)
        return SuccessResponse(serializer.data)
