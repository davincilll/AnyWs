from enum import Enum

from app.common.exceptionbox import base


class MissingRequiredParameterError(base.BadRequest400):

    def __init__(self, info=""):
        self.message = f"缺少必填参数{info}"


class NotAllowedParamsError(base.BadRequest400):
    def __init__(self, info=""):
        self.message = f"参数{info}不允许"


class ForbiddenError(base.Conflict409):
    def __init__(self, info=""):
        self.message = f"当前操作不允许,错误信息为{info}"


class InvalidParameterFormatError(base.BadRequest400):

    def __init__(self, info=""):
        self.message = f"参数{info}格式错误"


# 内部服务错误
class InternalServerError(base.InternalServerError500):
    def __init__(self, info=""):
        self.message = f"服务器内部错误,错误信息为{info},请联系系统管理员"


# 资源未找到错误
class ResourceNotFoundError(base.NotFound404):
    def __init__(self, info=""):
        self.message = f"资源未找到,错误信息为{info}"


class InvalidBusinessRequestErrorInfoEnum(Enum):
    """梳理各种业务请求的常量信息"""

    def __init__(self, code, message):
        self.code = code
        self.message = message


class InvalidBusinessRequestError(base.BadRequest400):
    def __init__(self, error_info: InvalidBusinessRequestErrorInfoEnum):
        self.code = error_info.code
        self.message = f"无效的业务请求，错误信息: {error_info.message}"

