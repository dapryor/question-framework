import os
import logging
from question_framework.question import Question, RepeatedQuestion, BranchedQuestion

script_dir = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger("question_framework")


def ask(questions: list):
    answerDicts = list(map(lambda q: q.ask(), questions))
    return {k: v for a in answerDicts for k, v in a.items()}
