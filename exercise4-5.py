counter = 0

while True:
    
    username = str(input("Enter username: "))
    password = str(input("Enter password: "))
    counter = counter + 1
    
    if username == "admin" and password == "0000":
        print("Welcome")
        break

    if counter > 4:
        print("Access denied")
        break

    if counter > 0:
        print("Incorrect, try again")

