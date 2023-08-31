zanderlen = float(input("Provide a length of a zander(cm): "))
if zanderlen < 42:
    print(f"Let the fish out into the sea. {42 - zanderlen} more cm to meet size limit.")
else:
    print("Size limit met")