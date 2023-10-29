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
    
class Race():
    def __init__(self, name: str, distance: int, cars: []) -> None:
        self.name = name
        self.distance = distance
        self.cars = cars
    def hour_passes(self):
        for car in self.cars:
            car.accelerate(random.randint(-10, 15))
            car.drive(1)
    def print_status(self):
        for car in self.cars:
            print(car)
    def race_finished(self):
        for car in self.cars:
            if car.travelled_distance >= self.distance:
                return True

race = Race("Grand Demolition Derby", 8000, [Car(f"ABC-{i}", random.randint(100, 200)) for i in range(10)])

hours = 0
while not race.race_finished():
    if hours % 10 == 0:
        race.print_status()
    race.hour_passes()
    hours += 1

race.print_status()
