import copy
from functools import wraps
from typing import Optional

from app.common.LoggerCenter import common_logger
from app.common.exceptionbox.errors import InternalServerError, MissingRequiredParameterError, NotAllowedParamsError


def router_register(router, basename=None):
    def decorator(cls):
        if basename is not None:
            _basename = basename
        else:
            _basename = None
            cls_name = cls.__name__

            # 判断类名是否包含 "ViewSet"
            if "ViewSet" in cls_name:
                common_logger.debug(f"{cls_name}开始注册")
                _basename = cls_name.split('ViewSet')[0]
                _basename = _basename[0:2].lower() + _basename[2:]  # 转换为小写
            elif "View" in cls_name:
                common_logger.debug(f"{cls_name}开始注册")
                _basename = cls_name.split('View')[0]
                _basename = _basename[0:2].lower() + _basename[2:]  # 转换为小写
            else:
                raise ValueError(f"{cls_name}不是有效的视图类名")
        if not any(item[0] == _basename for item in router.registry):
            router.register(_basename, cls, basename=_basename)
            common_logger.debug(f"Registered {_basename} with {cls}")
        else:
            common_logger.debug(f"{_basename} is already registered.")
        return cls

    return decorator


def params_check(required_params: Optional[list] = None, allowed_params: Optional[list] = None,
                 not_allowed_params: Optional[list] = None):
    """
    用于post参数过滤
    """
    if allowed_params and not_allowed_params:
        raise InternalServerError("allowedAndRequiredParams and notAllowedParams can not be set at the same time")

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            keys = set(request.data.keys()).union(set(request.query_params.dict()))
            AllowedParamsCopy = set(copy.deepcopy(allowed_params)) if allowed_params else set()
            notAllowedParamsCopy = set(copy.deepcopy(not_allowed_params)) if not_allowed_params else set()
            RequiredParamsCopy = set(copy.deepcopy(required_params)) if required_params else set()

            # 检查必需参数
            if RequiredParamsCopy:
                missing_params = RequiredParamsCopy - keys
                if missing_params:
                    raise MissingRequiredParameterError(info=list(missing_params))

            # 检查允许参数
            if AllowedParamsCopy:
                not_allowed = keys - AllowedParamsCopy
                if not_allowed:
                    raise NotAllowedParamsError(info=list(not_allowed))

            # 检查不允许参数
            if notAllowedParamsCopy:
                forbidden = keys & notAllowedParamsCopy
                if forbidden:
                    raise NotAllowedParamsError(info=list(forbidden))

            return view_func(self, request, *args, **kwargs)

        return wrapper

    return decorator
