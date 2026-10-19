import sys
import datetime
from functools import wraps

class DevLogger:
    def __init__(self, name="dev-toolkit-31"):
        self.name = name
        self.styles = {
            "info": "\033[94m",
            "error": "\033[91m",
            "success": "\033[92m",
            "reset": "\033[0m"
        }

    def log(self, message, level="info"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        style = self.styles.get(level, self.styles["reset"])
        print(f"{style}[{self.name}][{timestamp}] {message.upper()}{self.styles['reset']}", file=sys.stderr)

    def trap(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log(f"execution failure in {func.__name__}: {str(e)}", level="error")
                raise e
        return wrapper

# global logger instance
logger = DevLogger()

def log_call(func):
    return logger.trap(func)

def info(msg):
    logger.log(msg, "info")

def error(msg):
    logger.log(msg, "error")

def success(msg):
    logger.log(msg, "success")