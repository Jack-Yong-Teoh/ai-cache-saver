from functools import wraps
from app.utilities.export import prepare_streaming_response


def export_async(func):
    @wraps(func)
    async def _wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)

        if (
            "payload" in kwargs
            and hasattr(kwargs["payload"], "export")
            and kwargs["payload"].export is True
        ):
            result = prepare_streaming_response(result)

        return result

    return _wrapper
