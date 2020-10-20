import mock
import pytest
from question_framework.question import *
from question_framework.user_input import *


@pytest.fixture
def static_test_questions():
    return [
        BranchedQuestion("password?", "Do you want to enter a password? [y|n]", [
            Question("y", "What is your password?"),
            StaticAnswer("n", "They said no.")
        ]
        )
    ]


class TestAsk():

    def test_doc_example_1(self):

        with mock.patch("builtins.input", lambda x: 'foobar'):
            questions = [Question("Name", "Your name:")]
            answers = ask(questions)
            assert(answers == {"Name": "foobar"})

    def test_doc_example_2(self):

        repeat_input = mock.Mock()
        repeat_input.side_effect = ["321", "123", "765"]

        with mock.patch("builtins.input", repeat_input):
            questions = [RepeatedQuestion("Password", "Your password:", 3)]
            answers = ask(questions)
            assert(answers == {'Password': ['321', '123', '765']})

    def test_static_answer_1(self, static_test_questions):

        def answer_bank(key):
            return {
                "Do you want to enter a password? [y|n]\n": "y",
                "What is your password?\n": "123"
            }[key]

        with mock.patch("builtins.input", answer_bank):
            answers = ask(static_test_questions)
            assert(answers == {"password?": {"__answer": "y", "y": "123"}})

    def test_static_answer_2(self, static_test_questions):

        def answer_bank(key):
            return {
                "Do you want to enter a password? [y|n]\n": "n"
            }[key]

        with mock.patch("builtins.input", answer_bank):
            answers = ask(static_test_questions)
            assert(answers == {"password?": {
                   "__answer": "n", "n": "They said no."}})
