from question_framework.validation import isint

class Question:
    def __init__(self, name, text, verification=lambda x: x is not None, post_process=lambda x: x):
        self.name = name
        self.text = text
        self.verification = verification
        self.post_process = post_process

class RepeatedQuestion(Question):
    def __init__(self, name, text, repeated_questions, verification=isint, post_process=lambda x: int(x)):
        super(RepeatedQuestion, self).__init__(name, text, verification, post_process)
        self.repeated_questions = repeated_questions
