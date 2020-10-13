def ask(questions: list):
    answerDicts = map(lambda q: q.ask(), questions)
    return {k: v for a in answerDicts for k, v in a.items()}
