from httpx import Response
from typing import Callable, Any, Tuple, Coroutine
from datetime import datetime, timezone

def iso_time_now():
    time_now = datetime.now(timezone.utc)
    iso_time = time_now.isoformat(timespec="milliseconds")
    return iso_time.replace("+00:00", "Z")

async def measure_response_time(
    func: Callable,
    *args: Any,
    **kwargs: Any
) -> Tuple[str, float, Response]:
    """Measures time to compute of callable."""
    # Compute response time in UTC time
    start_time = datetime.now(timezone.utc)
    data : Response = await func(*args, **kwargs)
    end_time = datetime.now(timezone.utc)
    # Compute time delta and convert to seconds
    timedelta = end_time - start_time 
    duration = timedelta.total_seconds()  
    # Report time in ISO8061 and replace +00:00 with Z (Zulu)
    iso_start_time = start_time.isoformat(timespec="milliseconds")
    iso_start_time = iso_start_time.replace("+00:00", "Z")
    return iso_start_time, duration, data

async def request_options_chain(
    func: Callable,
    *args: Any,
    **kwargs: Any
) -> Coroutine[Any, Any, Response]:
    return await func(*args, **kwargs)