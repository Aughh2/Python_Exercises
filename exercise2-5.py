talents = float(input("Enter talents: "))
pounds = float(input("Enter pounds: "))
lots = float(input("Enter lots: "))

one_lot = 13.3
one_pound = one_lot * 32
one_talent = one_pound * 20

weight_in_grams = lots * one_lot + pounds * one_pound + talents * one_talent

print(f"The weight in modern units:\n{int(weight_in_grams/1000)} kilograms and {float(weight_in_grams%1000):.2f} grams.")