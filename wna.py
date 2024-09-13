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
    
    def window_middle_aisle_boarding(self):
        """Board passengers in the order of window (A, F), middle (B, E), then aisle (C, D), in descending row order."""
        window_seats = ['A', 'F']
        middle_seats = ['B', 'E']
        aisle_seats = ['C', 'D']
        
        window_passengers = [p for p in self.passengers if p.seat in window_seats]
        middle_passengers = [p for p in self.passengers if p.seat in middle_seats]
        aisle_passengers = [p for p in self.passengers if p.seat in aisle_seats]
        
        # Sort by row descending (50 -> 1)
        window_passengers.sort(key=lambda p: p.row, reverse=True)
        middle_passengers.sort(key=lambda p: p.row, reverse=True)
        aisle_passengers.sort(key=lambda p: p.row, reverse=True)
        
        # Combine the passengers in the order: window -> middle -> aisle
        self.passengers = window_passengers + middle_passengers + aisle_passengers
    
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

# Function to run the Window-Middle-Aisle Boarding simulation 100 times and plot the results
def run_wna_boarding_simulations(num_experiments=100):
    wna_times = []
    
    for _ in range(num_experiments):
        # Window-Middle-Aisle Boarding
        plane = Plane()
        plane.generate_passengers()
        plane.window_middle_aisle_boarding()
        wna_times.append(plane.board_passengers())
    
    # Convert list to NumPy array for easier manipulation
    wna_times = np.array(wna_times)
    
    # Calculate running mean
    wna_mean = np.cumsum(wna_times) / np.arange(1, num_experiments + 1)
    
    # Plot the results
    plt.plot(wna_mean, label='WNA (Window-Middle-Aisle)', color='red')
    
    plt.title('Mean Timer During Number of Experiments')
    plt.xlabel('Number of Experiments')
    plt.ylabel('Mean Timer')
    plt.legend()
    plt.show()

# Run the Window-Middle-Aisle Boarding simulation and plot the results
run_wna_boarding_simulations(100)
