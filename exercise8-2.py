import mysql.connector

db = mysql.connector.connect(
    host = "192.168.1.17", 
    port = 3306,
    database = "flight_game",
    user = "dbuser",
    password = "admin",
    autocommit = True
)

def getAirportsByCountryOrderByType(countrycode: str) -> []:
    sql = f"SELECT name, type FROM airport WHERE iso_country='{countrycode}' ORDER BY type;"
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

country = str(input("Please provide country code: "))
airports = getAirportsByCountryOrderByType(country)


for airport in airports:
    print(f"Name: {airport[0]}\nType: {airport[1]}\n")