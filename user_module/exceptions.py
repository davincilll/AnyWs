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


class VerificationCodeError(base.BadRequest400):
    """
    验证码错误
    """

    def __init__(self):
        self.message = "邮箱验证码错误"
