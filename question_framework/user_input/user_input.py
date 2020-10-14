def ask(questions: list):
    answer_dicts = map(lambda q: q.ask(), questions)
    return {k: v for a in answer_dicts for k, v in a.items()}
