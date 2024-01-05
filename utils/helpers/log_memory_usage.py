import psutil
import logging
import os


def log_memory_usage():
    """Logs the current memory usage of the script."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    logging.info(f"Memory Usage: {memory_info.rss / 1024 ** 2:.2f} MB")
