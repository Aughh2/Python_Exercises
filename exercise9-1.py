import random

class Car():
    def __init__(self, registration_number: str, max_speed: float) -> None:
        self.registration_number = registration_number
        self.max_speed = max_speed
        self.current_speed = 0
        self.travelled_distance = 0
    def __str__(self):
        string = f"{self.registration_number}|Max.Speed {self.max_speed}km/h|Speed {self.current_speed}km/h|Distance {self.travelled_distance}"
        return string

    def accelerate(self, speed_to_change: float):
        final_speed = self.current_speed + speed_to_change
        if final_speed < 0:
            final_speed = 0
        if final_speed > self.max_speed:
            final_speed = self.max_speed
        self.current_speed = final_speed
    def drive(self, hours: float):
        self.travelled_distance = self.travelled_distance + self.current_speed * hours
    

car1 = Car("ABC-123", 142)
print(car1)
car1.accelerate(30)
car1.accelerate(70)
car1.accelerate(50)
print(car1)
car1.accelerate(-200)
print(car1)

cars = [Car(f"ABC-{i}", random.randint(100, 200)) for i in range(10)]

def someone_drove_10000_km(cars: []) -> bool:
    for car in cars:
        if car.travelled_distance > 10000: return True
    return False

def everyone_accelerates(cars: []):
    for car in cars:
        car.accelerate(random.randint(-10, 15))
    
def everyone_drives_for_one_hour(cars: []):
    for car in cars:
        car.drive(1)

while True:
    if someone_drove_10000_km(cars): break
    everyone_accelerates(cars)
    everyone_drives_for_one_hour(cars)

for car in cars:
    print(car)