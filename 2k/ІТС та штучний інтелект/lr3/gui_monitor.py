
import tkinter as tk
from pymongo import MongoClient

client = MongoClient("mongodb+srv://fromartemm:jndDBPf9OOZkteUI@cluster0.fx4156z.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
db = client["transport_monitoring"]
collection = db["buses"]

def show_ships():
    ships = collection.find()
    for ship in ships:
        label = tk.Label(root, text=f"Судно {ship['ship_id']} ({ship['route']}): {ship['coordinates']} - Статус: {ship['status']}, Тех. стан: {ship['technical_state']}")
        label.pack()

root = tk.Tk()
root.title("Моніторинг суден")
root.geometry("500x400")
button = tk.Button(root, text="Показати всі судна", command=show_ships)
button.pack()
root.mainloop()
