import random


async def generate_captcha():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 9)
    operator = random.choice(["+", "-", "*"])
    question = f"{num1} {operator} {num2}"
    answer = str(eval(question))
    return question, answer
