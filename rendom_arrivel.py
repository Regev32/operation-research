import numpy as np
import random
import matplotlib.pyplot as plt

class Passenger:
    def __init__(self, row, seat):
        self.row = row
        self.seat = seat
        self.blocking_passengers = 0  # Number of passengers blocking the way
        self.time_to_seat = 0         # Total time taken to sit down
    
    def store_bag_time(self):
        """Time to store bag in the overhead compartment (exponentially distributed with a mean of 5 minutes)"""
        return np.random.exponential(5)
    
    def pass_blockers_time(self):
        """Time to pass blocking passengers (exponentially distributed with mean + 1 per blocking passenger)"""
        mean_time = 1 + self.blocking_passengers
        return np.random.exponential(mean_time)
    
    def settle_in_seat(self):
        """Simulates the process of the passenger taking their seat."""
        bag_time = self.store_bag_time()
        passing_time = self.pass_blockers_time()
        self.time_to_seat = bag_time + passing_time
        return self.time_to_seat

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
                self.add_passenger(passenger)
    
    def add_passenger(self, passenger):
        self.passengers.append(passenger)
    
    def random_boarding(self):
        """Randomize the boarding order of passengers."""
        random.shuffle(self.passengers)
    
    def board_passengers(self):
        """Simulates the boarding process for all passengers."""
        total_boarding_time = 0
        self.seated_passengers = set()  # Reset seated passengers each time
        
        for passenger in self.passengers:
            # Check for passengers already seated in the same row and blocking the way
            blocking_passengers = sum(
                1 for p in self.seated_passengers if p.row == passenger.row and p.seat < passenger.seat
            )
            passenger.blocking_passengers = blocking_passengers
            
            # The passenger settles in their seat
            time_to_seat = passenger.settle_in_seat()
            total_boarding_time += time_to_seat
            
            # Mark this passenger as seated
            self.seated_passengers.add(passenger)
        
        return total_boarding_time

# Function to run the Random Boarding simulation 100 times and plot the results
def run_random_boarding_simulations(num_experiments=100):
    random_times = []
    
    for _ in range(num_experiments):
        # Random Boarding
        plane = Plane()
        plane.generate_passengers()
        plane.random_boarding()
        random_times.append(plane.board_passengers())
    
    # Convert list to NumPy array for easier manipulation
    random_times = np.array(random_times)
    
    # Calculate running mean
    random_mean = np.cumsum(random_times) / np.arange(1, num_experiments + 1)
    
    # Plot the results
    plt.plot(random_mean, label='Random')
    
    plt.title('Mean Timer During Number of Experiments')
    plt.xlabel('Number of Experiments')
    plt.ylabel('Mean Timer')
    plt.legend()
    plt.show()

# Run the Random Boarding simulation and plot the results
run_random_boarding_simulations(100)
