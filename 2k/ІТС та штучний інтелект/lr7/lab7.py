import simpy
import random
import matplotlib.pyplot as plt

NUM_TRAINS = 3
NUM_PEDESTRIANS = 50
STATION_CAPACITY = 2
UNLOAD_TIME = 5
LOAD_TIME = 5
PEDESTRIAN_SPEED = [0.8, 1.2]
SIM_TIME = 60

pedestrian_log = []

class Train:
    def __init__(self, env, name, platform):
        self.env = env
        self.name = name
        self.platform = platform

    def serve(self):
        yield self.env.timeout(UNLOAD_TIME)
        yield self.env.timeout(LOAD_TIME)

class Pedestrian:
    def __init__(self, env, name, speed):
        self.env = env
        self.name = name
        self.speed = speed

    def move(self):
        time_to_exit = random.randint(10, 30) / self.speed
        yield self.env.timeout(time_to_exit)
        pedestrian_log.append((self.env.now, self.name))

def train_process(env, platforms):
    for i in range(1, NUM_TRAINS + 1):
        with platforms.request() as request:
            yield request
            train = Train(env, f'Train {i}', platforms.count)
            yield env.process(train.serve())

def pedestrian_process(env):
    for i in range(1, NUM_PEDESTRIANS + 1):
        speed = random.uniform(*PEDESTRIAN_SPEED)
        pedestrian = Pedestrian(env, f'Pedestrian {i}', speed)
        env.process(pedestrian.move())
        yield env.timeout(random.randint(1, 3))

def run_simulation():
    env = simpy.Environment()
    platforms = simpy.Resource(env, capacity=STATION_CAPACITY)
    env.process(train_process(env, platforms))
    env.process(pedestrian_process(env))
    env.run(until=SIM_TIME)
    return pedestrian_log

log = run_simulation()

time_series = list(range(SIM_TIME + 1))
passenger_count = []
for t in time_series:
    count = sum(1 for (exit_time, _) in log if exit_time >= t)
    passenger_count.append(count)

plt.figure(figsize=(10, 5))
plt.plot(time_series, passenger_count, label="Кількість пасажирів")
plt.xlabel("Час (хвилини)")
plt.ylabel("Кількість пасажирів у залі")
plt.title("Динаміка пасажиропотоку на вокзалі")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
