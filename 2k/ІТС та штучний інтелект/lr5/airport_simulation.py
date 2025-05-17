
import simpy
import random
import matplotlib.pyplot as plt

NUM_PARKING_SPOTS = 5
NUM_REFUEL_TRUCKS = 2
NUM_LOADERS = 3
SERVICE_TIME = {
    "refueling": (10, 20),
    "loading": (15, 25)
}
ARRIVAL_INTERVAL = (5, 15)

class Airport:
    def __init__(self, env):
        self.env = env
        self.parking_spots = simpy.Resource(env, NUM_PARKING_SPOTS)
        self.refuel_trucks = simpy.Resource(env, NUM_REFUEL_TRUCKS)
        self.loaders = simpy.Resource(env, NUM_LOADERS)

    def refuel_plane(self, plane_id):
        refuel_time = random.randint(*SERVICE_TIME["refueling"])
        yield self.env.timeout(refuel_time)

    def load_plane(self, plane_id):
        load_time = random.randint(*SERVICE_TIME["loading"])
        yield self.env.timeout(load_time)

def plane_process(env, plane_id, airport, log):
    arrival_time = env.now
    with airport.parking_spots.request() as parking_request:
        yield parking_request
        with airport.refuel_trucks.request() as refuel_request:
            yield refuel_request
            yield env.process(airport.refuel_plane(plane_id))
        with airport.loaders.request() as load_request:
            yield load_request
            yield env.process(airport.load_plane(plane_id))
    depart_time = env.now
    log.append(depart_time - arrival_time)

def generate_planes(env, airport, log):
    plane_id = 1
    while True:
        yield env.timeout(random.randint(*ARRIVAL_INTERVAL))
        env.process(plane_process(env, plane_id, airport, log))
        plane_id += 1

def main():
    print("Початок моделювання")
    random.seed(42)
    env = simpy.Environment()
    airport = Airport(env)
    log = []
    env.process(generate_planes(env, airport, log))
    env.run(until=120)
    print("Моделювання завершено")
    plt.hist(log, bins=10, color='skyblue', edgecolor='black')
    plt.title("Час обробки літаків")
    plt.xlabel("Хвилини")
    plt.ylabel("Кількість літаків")
    plt.grid(True)
    plt.savefig("airport_simulation_result.png")
    plt.show()

if __name__ == "__main__":
    main()
