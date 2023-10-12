import random
import sys

import mysql.connector
from geopy import distance

#Choose your own connection config
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
    #Generates a new available id based on amount of rows in game table
    sql = f"SELECT COUNT(id) FROM game"
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    newid = result[0] + 1
    return newid

def create_player(name: str) -> str:
    #Creates a player with a given name and id with 0 stats and at the starting location
    #returns player id if created sucessfully
    sql = f"INSERT INTO game (id, co2_consumed, co2_budget, location, screen_name) VALUES (%s, %s, %s, %s, %s)"
    cursor = db.cursor()
    ident = new_id()
    cursor.execute(sql, (ident, 0, 0, game_map[0], name))
    cursor.close()
    return ident

def get_player_location(playerid: str) -> str:
    #Fetches player location from database
    try:
        sql = f"SELECT location FROM game WHERE id=%s"
        cursor = db.cursor()
        cursor.execute(sql, (playerid, ))
        location = cursor.fetchone()
        cursor.close()
        return location[0]
    except:
        print("Error fetching given player's location")
        return ""

def get_players_next_location(playerid: str) -> str:
    try:
        current_location = get_player_location(playerid)
        current_index = game_map.index(current_location)
        next_index = current_index + 1
        next_icao = game_map[next_index]
        return next_icao
    except:
        print("Error getting player's next location.")
        return ""
    

def get_player_name(playerid: str) -> str:
    try:
        sql = f"SELECT screen_name FROM game WHERE id=%s"
        cursor = db.cursor()
        cursor.execute(sql, (playerid,))
        name = cursor.fetchone()
        cursor.close()
        return name[0]
    except:
        print("Wrong playerid provided to get player name")
        return ""

def roll_dice() -> int:
    return random.randint(1, 6)

def get_random_weather_condition() -> tuple:
    #Returns a random weather condition tuple where (name, description)
    sql = "SELECT name, description from GOAL"
    cursor = db.cursor()
    cursor.execute(sql)
    list_of_weather_conditions = cursor.fetchall()
    return random.choice(list_of_weather_conditions)

def player_won(playerid: str) -> bool:
    #Checks if player won
    try:
        if get_player_location(playerid) == game_map[len(game_map) - 1]:
            return True
        else:
            return False
    except:
        print("Wrong playerid provided to announce win.")
        return False
    
def get_co2_budget(playerid: str) -> int:
    try:
        sql = f"SELECT co2_budget FROM game WHERE id=%s"
        cursor = db.cursor()
        cursor.execute(sql, (playerid,))
        co2_budget = cursor.fetchone()
        cursor.close()
        return co2_budget[0]
    except:
        print("Wrong playerid provided to get co2 budget.")
        return 0


def add_to_co2_budget(playerid: str, value: int):
    try:
        sql = f"UPDATE game SET co2_budget=co2_budget+%s WHERE id=%s"
        cursor = db.cursor()
        cursor.execute(sql, (int(value), playerid))
        cursor.close()
        return
    except:
        print("Wrong playerid provided to add co2, or an invalid co2 value")

def get_airport_coordinates(icao: str) -> ():
    #Returns a tuple of latitude, longitude for the specified airport
    try:
        sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{icao}'"
        cursor = db.cursor()
        cursor.execute(sql)
        coordinates = cursor.fetchone()
        return coordinates
    except:
        print("Invalid icao to fetch coordinates.")
        return ()

def get_airport_name(icao: str) -> str:
    try:
        sql = f"SELECT name FROM airport WHERE ident=%s"
        cursor = db.cursor()
        cursor.execute(sql, (icao,))
        name = cursor.fetchone()
        cursor.close()
        return name[0]
    except:
        print("Invalid icao to fetch airport name.")
        return ""


def get_airport_country_name(icao: str) -> str:
    sql = "SELECT name FROM country WHERE iso_country IN (SELECT iso_country FROM airport WHERE ident=%s)"
    cursor = db.cursor()
    cursor.execute(sql, (icao,))
    country_name = cursor.fetchone()
    return country_name[0]

def calculate_distance(coordinates1: tuple, coordinates2: tuple) -> int:
    return int(distance.distance(coordinates1, coordinates2).km)

def calculate_co2_expenditure(distance:int, weather_tuple: tuple) -> int:
    #Check weather
    #weather tuple is a tuple where (name, description)
    expenditure = distance
    if weather_tuple[0] == "HOT" or weather_tuple[0] == "COLD":
        expenditure = distance * 1.2
    elif weather_tuple[0] == "0DEG" or weather_tuple[0] == "10DEG":
        expenditure = distance * 1.1
    elif weather_tuple[0] == "20DEG" or weather_tuple[0] == "CLEAR":
        expenditure = distance
    elif weather_tuple[0] == "CLOUDS" or weather_tuple[0] == "WINDY":
        expenditure == -1 # IF EXPENDITURE IS -1 then the player stays for one move
    return int(expenditure)

def co2_budget_is_enough_to_travel(c02_budget: int, co2_expenditure: float) -> bool:
    if c02_budget >= co2_expenditure:
        return True
    else:
        return False
    
def move_player(playerid: str, destination_icao: str, weather_tuple: tuple) -> bool:
    #Checks if players co2 budget is enough to travel and moves a player into the location
    #Returns false if failed due to insufficient c02 budget
    #Returns true if moved successfully

    #calculate distance between current location and destination
    current_location_icao = get_player_location(playerid)
    distance = calculate_distance(get_airport_coordinates(current_location_icao), get_airport_coordinates(destination_icao))
    
    #calculate c02 expenditure for a flight
    co2_expenditure = calculate_co2_expenditure(distance, weather_tuple)

    if not co2_budget_is_enough_to_travel(get_co2_budget(playerid), co2_expenditure):
        return False
    
    sql = f"UPDATE game SET co2_budget=co2_budget-%s, co2_consumed=co2_consumed+%s WHERE id=%s"
    cursor = db.cursor()
    try:
        cursor.execute(sql, (co2_expenditure, co2_expenditure, playerid))
        sql = f"UPDATE game SET location=%s WHERE id=%s"
        cursor.execute(sql, (destination_icao, playerid))
        return True
    except:
        print("Error moving player to the location.")

def player_wants_to_move(playerid: str) -> bool:
    while True:
        user_choice = input(f"{get_player_name(playerid)}, do you want to fly there? (y/n): ").strip().lower()
        if user_choice == 'y':
            return True
        elif user_choice == 'n':
            return False
        else:
            print("Invalid input. Try again.")

def bad_weather_prevents_a_flight(distance: float, weather_tuple: tuple) -> bool:
    if calculate_co2_expenditure(distance, weather_tuple) == -1:
        return True
    return False

def start_game():
    #Players are created in the beginning
    player1 = create_player(str(input("Please enter the name of the first player: "))) 
    player2 = create_player(str(input("Please enter the name of the second player: ")))
    #A list of two players is populated
    players = [player1, player2]

    while True: #Main loop
        #each player rolls the dice
        for player in players:
            print(f"{get_player_name(player)} rolls the dice...")
            input()
            dice_result = roll_dice()
            print(f"...{dice_result}")
            #players get co2 budget corresponding to the dice rolled
            co2_to_add = dice_result * 100
            add_to_co2_budget(player, co2_to_add)
            print(f"{get_player_name(player)} has a CO2 budget of {get_co2_budget(player)} now.")
            input()
            #Players get notified of their current location and destination
            next_destination = get_players_next_location(player)
            distance = calculate_distance(get_airport_coordinates(get_player_location(player)), get_airport_coordinates(next_destination))
            print(f"The next destination for {get_player_name(player)} is {get_airport_country_name(next_destination)}, {get_airport_name(next_destination)}.\n")
            print(f"The distance between current location and {get_airport_name(next_destination)} is {distance}.")

            #Get a weather condition
            weather_tuple = get_random_weather_condition()#Get a random weather tuple where (name, description)
            description = weather_tuple[1]
            print(f"The weather forecast shows '{description}.'")

            if bad_weather_prevents_a_flight(distance, weather_tuple):
                print(f"The weather is not suitable for a flight. {get_player_name(player)} waits for one move.")
                break

            print(f"The cost to move there condidering current weather conditions is {calculate_co2_expenditure(distance, weather_tuple)}.")

            #ask player if wants to move
            if not player_wants_to_move(player):
                continue
            

            #If player's move is doable with player's co2 budget
            if move_player(player, next_destination, weather_tuple):
                #Let a player know he reached the next destination
                print(f"{get_player_name(player)} reached {get_airport_country_name(next_destination)}!")
                #If player wins when moves to the destination - announce win and break from dice rolling loop
                if player_won(player):  
                    print(f"{get_player_name(player)} WON!")
                    break
            #If not enough co2 for the move, let the player know
            else:
                print(f"{get_player_name(player)} does not have enough CO2 budget. Wait for the next roll.")
            input()
        
        #If one of the players won - braak from the main loop
        if player_won(player1) or player_won(player2):
            break

#If this program is run, does what is below this statement
if __name__ == "__main__":
    start_game()