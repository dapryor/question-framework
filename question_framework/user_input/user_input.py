import os
from question_framework.question import Question, RepeatedQuestion, BranchedQuestion

script_dir = os.path.dirname(os.path.realpath(__file__))


def ask(questions: list):
    answerDicts = map(lambda q: q.ask(), questions)
    return {k: v for a in answerDicts for k, v in a.items()}
