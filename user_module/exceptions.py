from app.common.exceptionbox import base


class CaptchaError(base.BadRequest400):
    """
    验证码错误
    """

    def __init__(self):
        self.message = "验证码错误"


class EmailAlreadyExistsError(base.BadRequest400):
    """
    邮箱已存在
    """

    def __init__(self):
        self.message = "邮箱已存在"

class EmailNotExistsError(base.BadRequest400):
    """
    邮箱不存在
    """
    def __init__(self):
        self.message = "邮箱不存在"

class UsernameAlreadyExistsError(base.BadRequest400):
    """
    用户名已存在
    """
    def __init__(self):
        self.message = "用户名已存在"

class VerificationCodeError(base.BadRequest400):
    """
    验证码错误
    """

    def __init__(self):
        self.message = "邮箱验证码错误"


