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

###Notes
# Whether conditions will serve as traps:
# Depending on them the player has to spend more or less co2 budget, they are already stored in the db so we only have to fetch them
# Once we decide which whether conditions do what - we code it out, and the rest is to 
# let user choose continent;
# We could randomly get 12 or so LARGE airports from continent X and one max per country so that the game is different every time.
# So TODO list:
# * Come up with whether condition related bonuses and expenses
# * Implement continent choice
# * Maybe create some more settings like map size
###

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

def get_players_next_location(playerid: str) -> str:
    try:
        current_location = get_player_location(playerid)
        current_index = game_map.index(current_location)
        next_index = current_index + 1
        next_icao = game_map[next_index]
        return next_icao
    except:
        print("Error getting player's next location.")
    

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

def roll_dice() -> int:
    return random.randint(1, 6)

def player_won(playerid: str) -> bool:
    #Checks if player won
    try:
        if get_player_location(playerid) == game_map[len(game_map) - 1]:
            return True
        else:
            return False
    except:
        print("Wrong playerid provided to announce win.")
    
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
    try:
        cursor.execute(sql, (co2_expenditure, co2_expenditure, playerid))
        sql = f"UPDATE game SET location=%s WHERE id=%s"
        cursor.execute(sql, (destination_icao, playerid))
        return True
    except:
        print("Error moving player to the location.")

def start_game():
    player1 = create_player(str(input("Please enter the name of the first player: "))) 
    player2 = create_player(str(input("Please enter the name of the second player: ")))
    players = [player1, player2]

    while True:
        #players roll the dice
        
        for player in players:
            print(f"{get_player_name(player)} rolls the dice...")
            input()
            dice_result = roll_dice()
            print(f"...{dice_result}")
            #players get co2 budget corresponding to the dice rolled
            co2_to_add = dice_result * 100
            add_to_co2_budget(player, co2_to_add)
            print(f"{get_player_name(player)} has a CO2 budget of {get_co2_budget(player)}.")
            input()
            #Players get moved to their next destination if they have enough co2 budget
            next_destination = get_players_next_location(player)
            distance = calculate_distance(get_airport_coordinates(get_player_location(player)), get_airport_coordinates(next_destination))
            print(f"The next destination for {get_player_name(player)} is {get_airport_country(next_destination)}, {get_airport_name(next_destination)}.\nThe flight will cost {calculate_co2_expenditure(distance)} CO2 points.")
            input()
            if move_player(player, next_destination):
                print(f"{get_player_name(player)} reached {get_airport_country(next_destination)}!")
                if player_won(player):  
                    print(f"{get_player_name(player)} WON!")
                    break
            else:
                print(f"{get_player_name(player)} does not have enough CO2 budget. Wait for the next roll.")
            input()
        
        #If one of the players won-braak from the main loop
        if player_won(player1) or player_won(player2):
            break

def settings_menu() -> bool:
    #UNFINISHED, do not use
    OPTION_AMOUNT = 1
    print("1. Choose map")
    
    try:
        option = int(input("Type option: "))
    except ValueError:
        print("Invalid input value")
        settings_menu()

    if option < 1 or option > OPTION_AMOUNT:
        print("Invalid option choice")
        settings_menu()

    if option == "1":
        print("1. Europe")
        print("2. North America")
        print("3. South America")
        print("4. Asia")
        print("5. Africa")
        print("6. Oceania")

    return True

def main_menu() -> bool:
    #Lets user run the game and configure settings
    OPTION_AMOUNT = 3 
    print("1. Start game")
    print("2. Settings")
    print("3. Exit")
    
    try:
        option = int(input("Type option: "))
    except ValueError:
        print("Invalid input value")
        #Calls itself until correct option choice is received
        main_menu()

    if option < 1 or option > OPTION_AMOUNT:
        print("Invalid option choice")
        main_menu()
    
    if option == 1:
        start_game()
    if option == 2:
        #NOT USABLE YET
        settings_menu()
    if option == 3:
        sys.exit()
    return True
    
if __name__ == "__main__":
    main_menu()