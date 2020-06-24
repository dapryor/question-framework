import os
import logging

from question_framework.question import Question, RepeatedQuestion, BranchedQuestion
import logging

script_dir = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger("question_framework")

def ask_for_input(questions: list):
    def get_input_loop(question):
        tmp = None
        while tmp is None or not question.verification(tmp):
            tmp = input(question.text + "\n")
        return question.post_process(tmp)

    def loop_through_question(questions):
        ret = dict()
        if isinstance(questions, Question):
            questions = [questions]
        for question in questions:
            if isinstance(question, RepeatedQuestion):
                logger.debug(f"DEBUG: REPEAT Question: {question.name}")
                loop_cnt = get_input_loop(question)
                ret[question.name] = []
                for i in range(loop_cnt):
                    looped_answers = loop_through_question(question.repeated_questions)
                    ret[question.name].append(looped_answers)
            elif isinstance(question, BranchedQuestion):
                logger.debug(f"DEBUG: BRANCH Question: {question.name}")
                branch_answer = get_input_loop(question)
                ret[question.name] = loop_through_question(question.question_branches[branch_answer])
                ret[question.name]["__answer"] = branch_answer
            else:
                logger.debug(f"DEBUG: NORMAL Question: {question.name}")
                ret[question.name] = get_input_loop(question)
        return ret

    return loop_through_question(questions)
