class BusinessError(Exception):
    """业务异常基类"""
    def __init__(self, message='业务异常', code=400):
        self.message = message
        self.code = code
        super().__init__(message)

class ValidationError(BusinessError):
    """数据验证异常"""
    def __init__(self, message='数据验证失败'):
        super().__init__(message=message, code=400)

class PermissionError(BusinessError):
    """权限异常"""
    def __init__(self, message='权限不足'):
        super().__init__(message=message, code=403)

class NotFoundError(BusinessError):
    """资源不存在异常"""
    def __init__(self, message='资源不存在'):
        super().__init__(message=message, code=404) 