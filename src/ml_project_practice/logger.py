# To run this file: python src/ml_project_practice/logger.py

import os
import logging
from datetime import datetime

LOG_DIR = os.path.join(os.getcwd(), "logs")
# Create the log folder once, if it does not already exist.
os.makedirs(LOG_DIR, exist_ok=True)

# Give each program run its own timestamped log file.
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(
    # Include time, source line, module name, severity, and message in each entry.
    filename=LOG_FILE_PATH,
    format="[%(asctime)s %(lineno)d %(name)s - %(levelname)s - %(message)s]",
    level=logging.INFO,
    force=True,
)

# Other modules import this logger to write messages to the configured log file.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



