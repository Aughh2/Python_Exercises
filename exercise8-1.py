import mysql.connector

db = mysql.connector.connect(
    host = "192.168.1.17", 
    port = 3306,
    database = "flight_game",
    user = "dbuser",
    password = "admin",
    autocommit = True
)

def getAirportNameAndLocationByICAO(icao: str) -> ():
    sql = f"SELECT name, municipality FROM airport WHERE ident='{icao}'";
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return (result[0], result[1])

icao = str(input("Please provide the ICAO code to fetch the airport details: "))
name, city = getAirportNameAndLocationByICAO(icao)

print(f"Airport name: {name}\nCity: {city}")

