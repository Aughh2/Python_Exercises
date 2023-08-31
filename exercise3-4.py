try:
    year = int(input("Please specify a year: "))
    if not year % 4 == 0 or year % 400:
        print("The specified year is NOT a leap year")
    else:
        print("The specified year is a leap year")
except ValueError:
    print("Please provide an integer value for year")