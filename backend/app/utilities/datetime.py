from typing import Optional
from datetime import datetime


def str2date(
    string: str,
    raise_error: bool = True,
) -> Optional[datetime]:
    try:
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            return datetime.strptime(string, "%Y-%m-%d")
        except ValueError as e:
            if raise_error:
                raise e
    return None
