import random

def generate_points(N: int) -> list:
    """Generates a list of tuples which represent points"""
    l = []
    for i in range(0, N):
        l.append((random.uniform(-1,1), random.uniform(-1,1)))
    return l

N = int(input("How many points to generate?: "))
n = 0

listOfPoints = generate_points(N)

for point in listOfPoints:
    """If a point fullfills inequality then its inside of a circle"""
    if (point[0]**2 + point[1]**2) < 1:
        n = n + 1

pi = 4 * n / N

print(f"PI is approximately {pi}")