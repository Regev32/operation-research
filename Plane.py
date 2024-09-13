import numpy as np
import matplotlib.pyplot as plt

class Passenger:
    def __init__(self, row, seat):
        self.row = row
        self.seat = seat
        self.time_to_load_bag = np.random.exponential(5)  # Time to store bag in overhead compartment
        self.blocked = False  # Initially, the passenger is not blocked

class Plane:
    def __init__(self):
        self.passengers = []
        self.seated_passengers = set()  # Tracks which passengers are already seated
    
    def generate_passengers(self):
        """Generate a list of 300 passengers with seat assignments in rows 1-50 and seats A-F."""
        seats = ['A', 'B', 'C', 'D', 'E', 'F']
        for row in range(1, 51):  # Rows 1 to 50
            for seat in seats:    # Seats A to F
                passenger = Passenger(row, seat)
                self.passengers.append(passenger)
    
    def process_bag_loading(self):
        """Simulates the bag loading process for all passengers, with multiple passengers loading at once if possible."""
        time = 0
        queue = self.passengers.copy()  # Start with the full list of passengers in the queue

        while queue:
            # Find the passengers in the front who can load their bags (those not blocked by others)
            ready_to_load = []
            current_row = None
            
            for passenger in queue:
                if current_row is None or passenger.row != current_row:
                    ready_to_load.append(passenger)
                    current_row = passenger.row

            # Find the max bag loading time from the passengers who are ready
            if ready_to_load:
                max_bag_time = max(p.time_to_load_bag for p in ready_to_load)

                # Advance time by the max bag loading time (all ready passengers load in parallel)
                time += max_bag_time

                print(f"[DEBUG] Passengers loading bags in parallel, time += {max_bag_time:.2f} minutes")

                # Remove passengers who have finished loading their bags from the queue
                for passenger in ready_to_load:
                    queue.remove(passenger)
                    print(f"[DEBUG] Passenger in row {passenger.row}, seat {passenger.seat} finished loading bags")

            # Move the rest of the queue forward (next passengers get into position)
        
        return time

def plot_results(times, label, color):
    """Helper function to plot the cumulative mean results."""
    times = np.array(times)
    cumulative_mean = np.cumsum(times) / np.arange(1, len(times) + 1)
    plt.plot(cumulative_mean, label=label, color=color)
    plt.title('Mean Timer During Number of Experiments')
    plt.xlabel('Number of Experiments')
    plt.ylabel('Mean Timer')
    plt.legend()
    plt.show()

def simulate_bag_loading(num_experiments=100):
    """Run 100 trials to simulate the time for passengers to load their bags."""
    bag_loading_times = []

    for _ in range(num_experiments):
        plane = Plane()
        plane.generate_passengers()
        total_time = plane.process_bag_loading()
        bag_loading_times.append(total_time)
    
    # Plot the cumulative mean results
    plot_results(bag_loading_times, label="Bag Loading Time", color='blue')

# Run the simulation and plot the results
simulate_bag_loading(100)
