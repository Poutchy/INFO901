import functools
import logging
import threading
from datetime import datetime

# Configure once
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)


class Logger:
    """Utility class for decorating and logging methods with lock tracking."""

    @staticmethod
    def log_method(func):
        """Decorator to log method calls, arguments, return values, and locks."""

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            cls_name = self.__class__.__name__
            func_name = func.__name__
            start_time = datetime.now()

            logging.info(
                f"[{cls_name}.{func_name}] called with args={args}, kwargs={kwargs}"
            )

            try:
                result = func(self, *args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                logging.info(
                    f"[{cls_name}.{func_name}] returned {result!r} in {duration:.4f}s"
                )
                return result
            except Exception as e:
                logging.exception(f"[{cls_name}.{func_name}] raised {e}")
                raise

        return wrapper

    @staticmethod
    def log_lock(lock: threading.Lock, name: str = "Lock"):
        """Context manager to log lock acquisition/release."""

        class _LoggedLock:
            def __enter__(self_nonlocal):
                logging.debug(f"[{name}] trying to acquire...")
                lock.acquire()
                logging.debug(f"[{name}] acquired")
                return lock

            def __exit__(self_nonlocal, exc_type, exc_val, exc_tb):
                lock.release()
                logging.debug(f"[{name}] released")

        return _LoggedLock()
