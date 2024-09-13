import random
from Plane import Plane, plot_results

def run_random_boarding_simulation(num_experiments=100):
    random_times = []
    
    for _ in range(num_experiments):
        # Random Boarding
        plane = Plane()
        plane.generate_passengers()
        plane.random_boarding()

        # Simulate the bag loading process (randomly shuffled passengers)
        total_time = plane.process_bag_loading()
        random_times.append(total_time)
    
    # Plot results
    plot_results(random_times, label='Random', color='blue')

# Add random boarding logic to the Plane class
def random_boarding(self):
    """Randomize the boarding order of passengers."""
    random.shuffle(self.passengers)

# Monkey patch the Plane class to add random_boarding
Plane.random_boarding = random_boarding

if __name__ == '__main__':
    run_random_boarding_simulation()
