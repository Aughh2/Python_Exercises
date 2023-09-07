while True:
    inches = float(input("Give value in inches to convert to cm(negative number to quit): "))
    if inches < 0:
        break
    cm = inches * 2.54
    print(f"{inches} inches is {cm} cm.")