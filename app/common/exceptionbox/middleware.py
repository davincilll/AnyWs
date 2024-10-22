import json
import traceback

from django.http import JsonResponse

from .base import BaseReturn
from ..LoggerCenter import exception_logger


class ExceptionBoxMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    # noinspection PyMethodMayBeStatic
    def process_exception(self, request, exception):
        # 对于自定义的异常
        if issubclass(exception.__class__, BaseReturn):
            # 根据异常的状态码，来返回错误信息
            code = exception.code if hasattr(exception, 'code') else exception.__class__.__name__
            status_code = getattr(exception, 'status_code', 500)
            ret_json = {
                'code': code,
                'msg': getattr(exception, 'message', ''),
                'success': True if status_code < 400 else False,
                'data': {}
            }
            response = JsonResponse(ret_json, json_dumps_params={'ensure_ascii': False})
            # 确定记录的状态码
            response.status_code = status_code
            # 日志记录，这里是将内部网关错误进行记录，外部已知的错误不进行记录
            _logger = exception_logger.error if status_code >= 500 else exception_logger.warning
            _logger('status_code->{status_code}, error_code->{code} ,msg->{msg} , url->{url}, '
                    'method->{method}, param->{param}, '
                    'traceback->{traceback}'.format(
                status_code=status_code, code=ret_json['code'], url=request.path, msg=ret_json['msg'],
                method=request.method, param=json.dumps(getattr(request, request.method, {})),
                traceback=traceback.format_exc()
            ))
            return response
        # 对于其他异常进行处理，这些异常归类于系统内部异常
        else:
            ret_json = {
                'code': 'InternalServerError',
                'msg': getattr(exception, 'message', ''),
                'success': False,
                'data': {}
            }
            response = JsonResponse(ret_json)
            response.status_code = 500
            _logger = exception_logger.error
            _logger('status_code->{status_code}, error_code->{code},msg->{msg}, url->{url}, '
                    'method->{method}, param->{param}, '
                    'traceback->{traceback}'.format(
                status_code=response.status_code, code=ret_json['code'], url=request.path, msg=ret_json['msg'],
                method=request.method, param=json.dumps(getattr(request, request.method, {})),
                traceback=traceback.format_exc()
            ))
            return response
            pass
