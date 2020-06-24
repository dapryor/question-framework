from question_framework.validation import isint, pick_from_choices
import logging

logger = logging.getLogger("question_framework")

class Question:
    def __init__(self, name, text, validation=lambda x: x is not None, post_process=lambda x: x):
        self.name = name
        self.text = text
        self.verification = validation
        self.post_process = post_process

    def __hash__(self):
        return hash(self.name)


class RepeatedQuestion(Question):
    def __init__(self, name, text, repeated_questions,):
        super(RepeatedQuestion, self).__init__(name, text, isint, int)
        self.repeated_questions = repeated_questions


class BranchedQuestion(Question):
    def __init__(self, name, text, question_branches: list):
        question_dict = {q.name: q for q in question_branches}
        branched_validation = pick_from_choices(question_dict)
        super(BranchedQuestion, self).__init__(name, text, branched_validation)
        self.question_branches = question_dict
