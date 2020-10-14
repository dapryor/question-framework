import logging

from . import post_process, question, user_input, validation

logger = logging.getLogger("question_framework")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
