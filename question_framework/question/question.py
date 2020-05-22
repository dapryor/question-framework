from question_framework.validation import isint

class Question:
    def __init__(self, name, text, validation=lambda x: x is not None, post_process=lambda x: x):
        self.name = name
        self.text = text
        self.verification = validation
        self.post_process = post_process

class RepeatedQuestion(Question):
    def __init__(self, name, text, repeated_questions,):
        super(RepeatedQuestion, self).__init__(name, text, isint, int)
        self.repeated_questions = repeated_questions
