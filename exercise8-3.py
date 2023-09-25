import mysql.connector
from geopy import distance

db = mysql.connector.connect(
    host = "192.168.1.17", 
    port = 3306,
    database = "flight_game",
    user = "dbuser",
    password = "admin",
    autocommit = True
)

def getAirportCoordinates(icao: str) -> ():
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{icao}'"
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return result

def calculateDistance(coordinates1: tuple, coordinates2: tuple) -> float:
    return distance.distance(coordinates1, coordinates2).km

airport1 = str(input("Enter first airport icao: "))
airport2 = str(input("Enter second airport icao: "))

print(f"The distance between airports is {calculateDistance(getAirportCoordinates(airport1), getAirportCoordinates(airport2))}")
