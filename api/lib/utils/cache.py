import time
from functools import wraps

cache = {}

def cached(ttl=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key in cache and time.time() - cache[key]['time'] < ttl:
                return cache[key]['data']
            result = await func(*args, **kwargs)
            cache[key] = {'data': result, 'time': time.time()}
            return result
        return wrapper
    return decorator