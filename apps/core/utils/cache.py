from functools import wraps
from django.core.cache import cache
import hashlib
import json

def generate_cache_key(prefix, *args, **kwargs):
    """生成缓存键"""
    key_parts = [prefix]
    key_parts.extend(str(arg) for arg in args)
    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    key = ':'.join(key_parts)
    return hashlib.md5(key.encode()).hexdigest()

def cache_response(timeout=300, key_prefix='view'):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if request.method != 'GET':
                return func(self, request, *args, **kwargs)
            
            cache_key = generate_cache_key(
                key_prefix,
                request.path,
                request.GET.dict(),
                *args,
                **kwargs
            )
            
            response = cache.get(cache_key)
            if response is not None:
                return response
            
            response = func(self, request, *args, **kwargs)
            cache.set(cache_key, response, timeout)
            return response
        return wrapper
    return decorator 