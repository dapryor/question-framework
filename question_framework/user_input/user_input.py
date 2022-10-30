from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    from question_framework.question import Question

QuestionName = str


def ask(questions: List["Question"]) -> Dict[QuestionName, Any]:
    answer_dicts = map(lambda q: q.ask(), questions)
    return {k: v for a in answer_dicts for k, v in a.items()}
