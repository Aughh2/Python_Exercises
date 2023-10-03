import mysql.connector
import random
from geopy import distance

db = mysql.connector.connect(
    host = "192.168.1.17", 
    port = 3306,
    database = "flight_game",
    user = "dbuser",
    password = "admin",
    autocommit = True
)

game_map = ["LPPT", "LEMD", "LFML", "LIMC", "LOWW", "LZKZ", "UKBB", "UMMS", "EVRA", "EETN", "ULLI", "EFHK"]

def new_id() -> str:
    sql = f"SELECT COUNT(id) FROM game"
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    newid = result[0] + 1
    return newid

def create_player(name: str) -> str:
    #Creates a player with a given name and id with 0 stats and at the starting location
    #returns player id
    sql = f"INSERT INTO game (id, co2_consumed, co2_budget, location, screen_name) VALUES (%s, %s, %s, %s, %s)"
    cursor = db.cursor()
    ident = new_id()
    cursor.execute(sql, (ident, 0, 0, "LPPT", name))
    cursor.close()

    return ident

def get_player_location(playerid: str) -> str:
    sql = f"SELECT location FROM game WHERE id=%s"
    cursor = db.cursor()
    cursor.execute(sql, (playerid, ))
    location = cursor.fetchone()
    cursor.close()
    return location[0]

def get_players_next_location(playerid: str) -> str:
    current_location = get_player_location(playerid)
    current_index = game_map.index(current_location)
    next_index = current_index + 1
    next_icao = game_map[next_index]
    return next_icao
    

def get_player_name(playerid: str) -> str:
    sql = f"SELECT screen_name FROM game WHERE id=%s"
    cursor = db.cursor()
    cursor.execute(sql, (playerid,))
    name = cursor.fetchone()
    cursor.close()
    return name[0]

def roll_dice() -> int:
    return random.randint(1, 6)

def get_co2_budget(playerid: str) -> int:
    sql = f"SELECT co2_budget FROM game WHERE id=%s"
    cursor = db.cursor()
    cursor.execute(sql, (playerid,))
    co2_budget = cursor.fetchone()
    cursor.close()
    return co2_budget[0]

def add_to_co2_budget(playerid: str, value: int):
    sql = f"UPDATE game SET co2_budget=co2_budget+%s WHERE id=%s"
    cursor = db.cursor()
    cursor.execute(sql, (int(value), playerid))
    cursor.close()
    return

def get_airport_coordinates(icao: str) -> ():
    #Returns a tuple of latitude, longitude for the specified airport
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{icao}'"
    cursor = db.cursor()
    cursor.execute(sql)
    coordinates = cursor.fetchone()
    return coordinates

def get_airport_name(icao: str) -> str:
    sql = f"SELECT name FROM airport WHERE ident=%s"
    cursor = db.cursor()
    cursor.execute(sql, (icao,))
    name = cursor.fetchone()
    cursor.close()
    return name[0]

def get_airport_country(icao: str) -> str:
    sql = f"SELECT iso_country FROM airport WHERE ident=%s"
    cursor = db.cursor()
    cursor.execute(sql, (icao,))
    country_name = cursor.fetchone()
    return country_name[0]

def calculate_distance(coordinates1: tuple, coordinates2: tuple) -> int:
    return int(distance.distance(coordinates1, coordinates2).km)

def calculate_co2_expenditure(distance:int) -> int:
    return distance

def co2_budget_is_enough_to_travel(c02_budget: int, distance: float) -> bool:
    if c02_budget >= distance:
        return True
    else:
        return False
    
def move_player(playerid: str, destination_icao: str) -> bool:
    #Checks if players co2 budget is enough to travel and moves a player into the location
    #Returns false if failed due to insufficient c02 budget
    #Returns true if moved successfully

    #calculate distance between current location and destination
    current_location_icao = get_player_location(playerid)
    distance = calculate_distance(get_airport_coordinates(current_location_icao), get_airport_coordinates(destination_icao))

    if not co2_budget_is_enough_to_travel(get_co2_budget(playerid), distance):
        return False
    
    #calculate c02 expenditure for a flight
    co2_expenditure = calculate_co2_expenditure(distance)
    sql = f"UPDATE game SET co2_budget=co2_budget-%s, co2_consumed=co2_consumed+%s WHERE id=%s"
    cursor = db.cursor()
    cursor.execute(sql, (co2_expenditure, co2_expenditure, playerid))
    sql = f"UPDATE game SET location=%s WHERE id=%s"
    cursor.execute(sql, (destination_icao, playerid))
    return True

def main():
    player1 = create_player(str(input("Please enter the name of the first player: "))) 
    player2 = create_player(str(input("Please enter the name of the second player: ")))
    players = [player1, player2]

    while True:
        #players roll the dice
        #players get co2 budget corresponding to the dice rolled
        for player in players:
            if get_player_location(player) == "EFHK":
                print(f"{get_player_name(player)} WON!")
                break
            print(f"{get_player_name(player)} rolls the dice...")
            input()
            dice_result = roll_dice()
            print(f"...{dice_result}")

            co2_to_add = dice_result * 100
            add_to_co2_budget(player, co2_to_add)
            print(f"{get_player_name(player)} has a CO2 budget of {get_co2_budget(player)}.")
            input()

            next_destination = get_players_next_location(player)
            distance = calculate_distance(get_airport_coordinates(get_player_location(player)), get_airport_coordinates(next_destination))
            print(f"The next destination for {get_player_name(player)} is {get_airport_country(next_destination)}, {get_airport_name(next_destination)}.\nThe flight will cost {calculate_co2_expenditure(distance)} CO2 points.")
            input()
            if move_player(player, next_destination):
                print(f"{get_player_name(player)} reached {get_airport_country(next_destination)}!")
            else:
                print(f"{get_player_name(player)} does not have enough CO2 budget. Wait for the next roll.")
            input()
        

if __name__ == "__main__":
    main()

