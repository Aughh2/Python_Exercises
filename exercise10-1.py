class Elevator():
    def __init__(self, bottom: int, top: int) -> None:
        self.bottom_floor = bottom
        self.top_floor = top
        self.floor = bottom
    
    def floor_up(self):
        if self.floor != self.top_floor:
            self.floor += 1
        
    def floor_down(self):
        if self.floor != self.bottom_floor:
            self.floor -= 1
    
    def go_to_floor(self, floor: int):
        print(f"Floor {self.floor}")
        if self.floor == floor:
            return
        if self.floor < floor: 
            self.floor_up()
            return self.go_to_floor(floor)
        if self.floor > floor:
            self.floor_down()
            return self.go_to_floor(floor)

class Building():
    def __init__(self, bottom: int, top: int, elevators_num: int) -> None:
        self.bottom = bottom
        self.top = top
        self.elevators_num = elevators_num
        self.elevators = [Elevator(bottom,top) for e in range(elevators_num)]
    
    def run_elevator(self, elevator_index: int, destination_floor: int):
        elevator = self.elevators[elevator_index]
        elevator.go_to_floor(destination_floor)

    def fire_alarm(self):
        for elevator in self.elevators: 
            elevator.go_to_floor(self.bottom)

#lift = Elevator(-1, 10)
#lift.go_to_floor(10)
#lift.go_to_floor(6)

b1 = Building(-3, 20, 5)

b1.run_elevator(4, 5)
b1.run_elevator(1, 4)
b1.run_elevator(4, 1)

b1.fire_alarm()