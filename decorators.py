import time
import pickle
import os
from functools import wraps
import exceptions


def rate_limited(max_per_interval, interval="second"):
    def decorator(func):
        # Initialize counter and last_called timestamp
        counter = 0
        last_called = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal counter, last_called
            current_time = time.time()

            # Determine the interval in seconds
            interval_seconds = 60 if interval == "minute" else 1

            # Reset counter and last_called if interval has passed
            if current_time - last_called >= interval_seconds:
                counter = 0
                last_called = current_time

            # Check if the function can be called
            if counter >= max_per_interval:
                raise exceptions.RateLimitExceeded()

            # Increment counter and call the function
            counter += 1
            return func(*args, **kwargs)

        return wrapper

    return decorator


def time_based_cache(timeout, cache_file="cache.pkl"):
    def decorator(func):
        def wrapper(*args):
            # Initialize an empty cache dictionary
            cache = {}

            # Load existing cache from file, if it exists
            if os.path.exists(cache_file):
                with open(cache_file, "rb") as f:
                    cache = pickle.load(f)

            # Check if args are already cached
            if args in cache:
                last_time, result = cache[args]
                # Check if the cache is within the timeout period
                if time.time() - last_time < timeout:
                    return result

            # Execute the function and cache the result
            result = func(*args)
            cache[args] = (time.time(), result)

            # Save cache to file
            with open(cache_file, "wb") as f:
                pickle.dump(cache, f)

            return result

        return wrapper

    return decorator
