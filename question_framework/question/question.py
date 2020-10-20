import logging

from question_framework.validation import pick_from_choices, ValidationError

logger = logging.getLogger("question_framework")


class Question:
    def __init__(self, name, text, validation=lambda x: x is not None, post_process=lambda x: x):
        self.name = name
        self.text = text
        self.validation = validation
        self.post_process = post_process

    def __hash__(self):
        return hash(self.name)

    def get_answer(self):
        while True:
            answer = input(self.text + "\n")
            try:
                valid = self.validation(answer)
            except ValidationError as err:
                # TODO: Allow an end user to output somewhere other than stdout
                print(err)
                continue

            if valid is True:
                break

        return self.post_process(answer)

    def ask(self):
        logger.debug(f"Question: {self.name}")
        return {self.name: self.get_answer()}


class RepeatedQuestion(Question):
    def __init__(self, name, text, ask_count, validation=lambda x: x is not None, post_process=lambda x: x):
        super(RepeatedQuestion, self).__init__(name, text, validation=validation, post_process=post_process)
        self.ask_count = ask_count

    def ask(self):
        logger.debug(f"REPEAT Question: {self.name}")
        return {self.name: list(map(lambda q: q.get_answer(), [self] * self.ask_count))}


class BranchedQuestion(Question):
    def __init__(self, name, text, question_branches: list):
        question_dict = {q.name: q for q in question_branches}
        branched_validation = pick_from_choices(question_dict)
        super(BranchedQuestion, self).__init__(name, text, branched_validation)
        self.question_branches = question_dict

    def ask(self):
        logger.debug(f"BRANCH Question: {self.name}")
        ret = dict()
        branch_answer = self.get_answer()
        ret[self.name] = self.question_branches[branch_answer].ask()
        ret[self.name]["__answer"] = branch_answer
        return ret
