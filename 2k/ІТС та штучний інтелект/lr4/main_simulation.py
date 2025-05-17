import simpy
import random
import statistics
from visualization import visualize_results
from results_export import save_results_to_csv

NUM_BOOTHS = 3
CARS_PER_HOUR = 100
SIMULATION_TIME = 2 * 60
PAYMENT_TIME = 2

wait_times = []

def pay_toll(car_id, env, toll_booths):
    global wait_times
    arrival_time = env.now
    with toll_booths.request() as request:
        yield request
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        yield env.timeout(random.expovariate(1.0 / PAYMENT_TIME))

def car_generator(env, toll_booths):
    car_id = 0
    while True:
        if 30 <= env.now <= 60:
            rate = CARS_PER_HOUR * 1.5
        else:
            rate = CARS_PER_HOUR
        yield env.timeout(random.expovariate(rate / 60.0))
        car_id += 1
        env.process(pay_toll(car_id, env, toll_booths))

def analyze_results():
    avg_wait_time = statistics.mean(wait_times)
    max_wait_time = max(wait_times)
    print(f"Середній час очікування: {avg_wait_time:.2f} хв")
    print(f"Максимальний час очікування: {max_wait_time:.2f} хв")

def run_simulation():
    env = simpy.Environment()
    toll_booths = simpy.Resource(env, capacity=NUM_BOOTHS)
    env.process(car_generator(env, toll_booths))
    env.run(until=SIMULATION_TIME)
    analyze_results()
    visualize_results(wait_times)
    save_results_to_csv(wait_times)

if __name__ == "__main__":
    run_simulation()