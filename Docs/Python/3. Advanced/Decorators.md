# Base
- **Common**
```python
import functools


def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        return result
    return wrapper
```
- **Parameterized**
```python
def arg_decorator(*dec_args, **dec_kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):

            result = func(*args, **kwargs)

            return result
        return wrapper
    return decorator
```