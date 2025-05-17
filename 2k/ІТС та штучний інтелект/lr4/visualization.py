import matplotlib.pyplot as plt

def visualize_results(wait_times):
    plt.hist(wait_times, bins=10, edgecolor='black')
    plt.title("Розподіл часу очікування")
    plt.xlabel("Час очікування (хв)")
    plt.ylabel("Кількість автомобілів")
    plt.tight_layout()
    plt.savefig("wait_time_distribution.png")
    plt.show()