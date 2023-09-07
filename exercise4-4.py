import random

number = random.randint(1, 10)
guess = 0

while guess != number:
    guess = int(input("Guess an int(1-10): "))
    if guess < 1 or guess > 10:
        print("Wrong number")
    elif guess < number:
        print("Too low")
    elif guess > number:
        print("Too high")

print(f"Good job! It was {number}")