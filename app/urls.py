import importlib
import inspect

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.views import LoginView
from django.urls import path, include, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app.common.utils.viewset_auto_discovery import ScanHelper

installed_app = settings.INSTALLED_APPS
ScanHelper(installed_app).scan_only_once()

schema_view = get_schema_view(
    openapi.Info(
        title="AnyWs",
        default_version="v1",
        description="一个网页浏览器插件添加单词的后端",
        # 指定API的服务条款URL
        terms_of_service="API 遵循 REST标准进行设计。我们的 API是可预期的以及面向资源的",
        contact=openapi.Contact(email="3135287831@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    authentication_classes=[SessionAuthentication],
    permission_classes=[IsAdminUser],
    public=True
)


def scan_and_register_routes():
    # route_prefix = settings.ROUTE_PREFIX
    _urlpatterns = []
    # dir_path = os.path.dirname(__file__)
    # 导入 routers.py 文件
    module = importlib.import_module('app.routers')  # 替换为实际模块名

    # 遍历模块中的所有对象
    for name, obj in inspect.getmembers(module):
        # 检查对象是否是 DefaultRouter 的实例
        if isinstance(obj, DefaultRouter):
            # 移除 'router' 后缀
            prefix = name.replace('_router', '')  # 去掉 '_router' 后缀
            _urlpatterns.append(path(f'{prefix}/', include(obj.urls)))

    return _urlpatterns


def get_urlpatterns():
    _urlpatterns = [
        path('admin/', admin.site.urls),
        # 增加验证码的视图
        path('captcha/', include('captcha.urls')),
        path(f'auth/', include('rest_framework.urls', namespace='rest_framework')),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),  # 用于静态的文件
        # 增加用户登录接口
        path('token/access_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        # refresh_token理由，默认的有效期为24小时,这里改为了15天
        path('token/refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
        path("docs/", permission_required("schema-swagger-ui")(schema_view.with_ui("swagger", cache_timeout=0))),
        path("docs/login/", LoginView.as_view(template_name='admin/login.html'), name="docs-login"),
        path("docs/logout", LoginView.as_view(template_name='admin/login.html'), name="docs-logout"),
        path('user_module/', include('user_module.urls', namespace='user_module')),
        path('translation_module/', include('translation_module.urls', namespace='translation_module'))
    ]
    if settings.DEBUG:
        import debug_toolbar
        _urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
    _urlpatterns += scan_and_register_routes()
    return _urlpatterns


urlpatterns = get_urlpatterns()
