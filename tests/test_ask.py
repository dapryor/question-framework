import mock
from question_framework.question import *
from question_framework.user_input import *


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
