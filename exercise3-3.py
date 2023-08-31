def check_hemoglobin(gender: str, hemoglobin: float) -> str:
    if (gender == "m" and hemoglobin < 134) or (gender == "f" and hemoglobin < 117):
        return "low"
    if (gender == "m" and hemoglobin > 134 and hemoglobin < 167) or (gender == "f" and hemoglobin > 117 and hemoglobin < 155):
        return "normal"
    if (gender == "m" and hemoglobin > 167) or (gender == "f" and hemoglobin > 155):
        return "high"

gender = str(input("Your gender(m/f): "))
if not (gender=="m" or gender=="f"):
    print("Invalid gender")
hem = float(input("Provide hemoglobin value (g/l): "))

print(check_hemoglobin(gender, hem))