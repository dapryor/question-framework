<p align="center">
  <img height="200px" src="https://raw.githubusercontent.com/dapryor/question-framework/master/assets/logo.png">
</p>
<p align="center">
       <b>Question Framework helps you to ask questions and get answers in a declarative way!</b>
</p>

<p align="center">
  <a href="https://github.com/dapryor/question-framework/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/dapryor/question-framework.svg">
  </a>
</p>

# Question Framework

## Basic Usage

```python
from question_framework.question import Question, RepeatedQuestion, BranchedQuestion
from question_framework.user_input import ask

questions = [Question("Name", "Your name:")]
answers = ask(questions)
print(answers)
```

Output:
```bash
Your name:
foobar
{'Name': 'foobar'}
```


## Question Types

### Question
`Question` is basically a question with an answer.
```python
questions = [Question("Name", "Your name:")]
answers = ask(questions)
print(answers)
```

Output:
```bash
Your name:
John Doe
{'Name': 'John Doe'}
```

### Repeated Question
`RepeatedQuestion` can be used to ask same question consecutively.

```python
questions = [RepeatedQuestion("Password", "Your password:", 2)]
answers = ask(questions)
print(answers)
```

Output:
```bash
Your password:
123
Your password:
321
Your password:
765
{'Password': ['123', '321', '765']}
```

### Branched Question
`BranchedQuestion` can be used to create one way adventures.

```python
game = [BranchedQuestion("Main", "Where to go? [N | E | S | W]", [
    Question("N", "North is cold. You died! (type anything to exit)"),
    Question("E", "You trigerred the trap. (type anything to exit)"),
    BranchedQuestion("S", "You found a tresure chest! [open | leave]", [
        Question("open", "It was a trap! (type anything to exit)"),
        Question("leave", "You leave the cave.. (type anything to exit)"),
    ]),
    Question("W", "West is wild, you died! (type anything to exit)"),
])]
answers = ask(game)
```

## Validations

A validation function can be specified to validate answers. If validation fails, user will be asked to enter the input again.
```python
Question("Password", "Enter password:", validation=lambda x: len(x) > 5)
```

## Post process

A post process can be specified to transform answer.
```python
Question("Firstname", "Enter firstname:", post_process=lambda x: x.upper())
```
