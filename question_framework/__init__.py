from . import post_process, question, user_input, validation
import logging

logger = logging.getLogger("question_framework")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)


