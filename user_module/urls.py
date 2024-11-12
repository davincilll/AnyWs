from django.urls import path

from user_module.views.UserViewSet import register, get_captcha

app_name = 'user_module'
urlpatterns = [
    # path('modify-password/', modify_pwd, name='modify-password'),  # URL 配置
    path('register/', register, name='register'),
    # path('send-register-verification-code/', send_register_verification_code, name='send-register-verification-code'),
    # path('send-modify-pwd-verification-code/', send_modify_pwd_verification_code,
    #      name='send-modify-pwd-verification-code'),
    path('captcha/', get_captcha, name='captcha'),
]
