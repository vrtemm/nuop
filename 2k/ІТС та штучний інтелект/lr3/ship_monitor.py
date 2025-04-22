
from pymongo import MongoClient

client = MongoClient("mongodb+srv://fromartemm:jndDBPf9OOZkteUI@cluster0.fx4156z.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
db = client["transport_monitoring"]
collection = db["buses"]

def get_ships():
    ships = collection.find()
    for ship in ships:
        print(f"Судно {ship['ship_id']} ({ship['route']}): {ship['coordinates']} - Статус: {ship['status']}, Тех. стан: {ship['technical_state']}")

def update_ship_location(ship_id, lat, lon):
    collection.update_one(
        {"ship_id": ship_id},
        {"$set": {"coordinates": {"latitude": lat, "longitude": lon}}}
    )
    print(f"Координати судна {ship_id} оновлено!")

def update_technical_state(ship_id, state):
    collection.update_one(
        {"ship_id": ship_id},
        {"$set": {"technical_state": state}}
    )
    print(f"Технічний стан судна {ship_id} оновлено!")

# Тестовий запуск
get_ships()
update_ship_location("SHIP001", 46.5000, 30.7500)
