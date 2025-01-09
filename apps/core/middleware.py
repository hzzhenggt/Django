from django.http import JsonResponse
from .exceptions import BusinessError
import logging

logger = logging.getLogger(__name__)

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        """处理异常"""
        if isinstance(exception, BusinessError):
            return JsonResponse({
                'code': exception.code,
                'message': str(exception),
                'data': None
            }, status=exception.code)
        
        # 记录未知异常
        logger.error(f"Unhandled exception: {str(exception)}", exc_info=True)
        return JsonResponse({
            'code': 500,
            'message': '服务器内部错误',
            'data': None
        }, status=500) 