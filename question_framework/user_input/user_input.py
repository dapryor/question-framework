import os

from jinja2 import Environment, FileSystemLoader

from question_framework import package
from question_framework.question import Question, RepeatedQuestion
from question_framework.validation import *


script_dir = os.path.dirname(os.path.realpath(__file__))


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
                loop_cnt = get_input_loop(question)
                ret[question.name] = []
                for i in range(loop_cnt):
                    looped_answers = loop_through_question(question.repeated_questions)
                    ret[question.name].append(looped_answers)
            else:
                ret[question.name] = get_input_loop(question)
        return ret

    return loop_through_question(questions)


def choose_package():
    package_name = package.package_names()
    package_choice = Question("package choice",
                               "What configuration file do you want to build? {}".format(package_name),
                               pick_from_choices(*package_name))

    user_in = ask_for_input(package_choice)
    return user_in["package choice"]


def render(package, template_vars):
    template_loader = FileSystemLoader(searchpath=package.template_dir)
    env = Environment(
        loader=template_loader,
    )
    template_renders = []
    for template in package.templates:
        template_obj = env.get_template(template)
        template_renders.append(template_obj.render(**template_vars))

    return template_renders


def save(template_renders):
    output_dir = os.environ["CONFIG_TOOL_OUTPUT_DIR"]
    for text in template_renders:
        with open(os.path.join(output_dir, "test"), "w") as f:
            f.write(text)


