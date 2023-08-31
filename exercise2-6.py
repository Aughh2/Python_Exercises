import random

def threeDigitCode() -> str:
    code = []
    for num in range(3):
        num = random.randint(0, 9)
        code.append(str(num))
    return "".join(code)

def fourDigitCode() -> str:
    code = []
    for num in range(4):
        num = random.randint(1, 6)
        code.append(str(num))
    return "".join(code)

print(f"Three digit code: {threeDigitCode()}\nFour digit code: {fourDigitCode()}")