from pymongo import MongoClient

client = MongoClient("mongodb+srv://fromartemm:jndDBPf9OOZkteUI@cluster0.fx4156z.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
db = client["transport_monitoring"]
collection = db["buses"]

ships = [
    {
        "ship_id": "SHIP001",
        "route": "Одеса — Стамбул",
        "coordinates": {"latitude": 46.4825, "longitude": 30.7233},
        "status": "on_route",
        "technical_state": "good",
        "arrival_time": "2024-04-17T15:30:00"
    },
    {
        "ship_id": "SHIP002",
        "route": "Херсон — Констанца",
        "coordinates": {"latitude": 46.6350, "longitude": 32.6169},
        "status": "delayed",
        "technical_state": "needs_maintenance",
        "arrival_time": "2024-04-17T18:00:00"
    }
]

collection.insert_many(ships)
print("Дані про судна додано до бази!")
