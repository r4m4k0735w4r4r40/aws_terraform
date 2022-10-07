import json
import logging

logger = logging.getLogger(__name__)
LOG_LEVEL = "INFO"
logger.setLevel(LOG_LEVEL)

def lambda_handler(event,context):
    logger.info(event)
    logger.info("Function invoked successfully.")

