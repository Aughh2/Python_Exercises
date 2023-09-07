numlist = []
while True:
    string = str(input("Enter a number(empty string to quit): "))
    if string == "":
        break
    numlist.append(float(string))

print(f"Min is {min(numlist)}\nMax is {max(numlist)}")
