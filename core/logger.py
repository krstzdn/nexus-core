"""
NEXUS Logger Subsystem
Prevents duplicate handler registration and structures core logs with dynamic naming.
"""
import logging
import sys

class Logger:
    def __init__(self, name="NEXUS"):
        # Artık hem boş çağrıları hem de Logger("NEXUS-CORE") gibi isimlendirmeleri kabul eder.
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if self.logger.handlers:
            return

        formatter = logging.Formatter(
            fmt="%(asctime)s - [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)