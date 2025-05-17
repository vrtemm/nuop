import csv

def save_results_to_csv(wait_times):
    with open("simulation_results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Car ID", "Wait Time"])
        for car_id, wait_time in enumerate(wait_times, 1):
            writer.writerow([car_id, wait_time])