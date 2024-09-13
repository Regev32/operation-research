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
    
    def ascending_boarding(self):
        """Board passengers in ascending order of rows, with random seat order in each row."""
        self.passengers.sort(key=lambda p: p.row)
        self._shuffle_seats_within_rows()

    def descending_boarding(self):
        """Board passengers in descending order of rows, with random seat order in each row."""
        self.passengers.sort(key=lambda p: p.row, reverse=True)
        self._shuffle_seats_within_rows()
    
    def _shuffle_seats_within_rows(self):
        """Shuffles the seat order within each row while maintaining row order."""
        current_row = None
        row_group = []
        shuffled_passengers = []
        
        # Shuffle passengers within the same row
        for passenger in self.passengers:
            if passenger.row != current_row:
                if row_group:
                    random.shuffle(row_group)
                    shuffled_passengers.extend(row_group)
                current_row = passenger.row
                row_group = [passenger]
            else:
                row_group.append(passenger)
        
        if row_group:
            random.shuffle(row_group)
            shuffled_passengers.extend(row_group)
        
        self.passengers = shuffled_passengers
    
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

# Function to run the simulation 100 times for each boarding method and plot the results
def run_simulations(num_experiments=100):
    random_times = []
    ascending_times = []
    descending_times = []
    wna_times = []
    
    for _ in range(num_experiments):
        # Random Boarding
        plane = Plane()
        plane.generate_passengers()
        plane.random_boarding()
        random_times.append(plane.board_passengers())
        
        # Ascending Boarding
        plane = Plane()
        plane.generate_passengers()
        plane.ascending_boarding()
        ascending_times.append(plane.board_passengers())
        
        # Descending Boarding
        plane = Plane()
        plane.generate_passengers()
        plane.descending_boarding()
        descending_times.append(plane.board_passengers())
        
        # WNA Boarding (Window-Middle-Aisle)
        plane = Plane()
        plane.generate_passengers()
        plane.window_middle_aisle_boarding()
        wna_times.append(plane.board_passengers())
    
    # Convert lists to NumPy arrays for easier manipulation
    random_times = np.array(random_times)
    ascending_times = np.array(ascending_times)
    descending_times = np.array(descending_times)
    wna_times = np.array(wna_times)
    
    # Calculate running means
    random_mean = np.cumsum(random_times) / np.arange(1, num_experiments + 1)
    ascending_mean = np.cumsum(ascending_times) / np.arange(1, num_experiments + 1)
    descending_mean = np.cumsum(descending_times) / np.arange(1, num_experiments + 1)
    wna_mean = np.cumsum(wna_times) / np.arange(1, num_experiments + 1)
    
    # Plot the results
    plt.plot(random_mean, label='Random')
    plt.plot(ascending_mean, label='First Rows')
    plt.plot(descending_mean, label='Last Rows')
    plt.plot(wna_mean, label='WNA (Window-Middle-Aisle)', color='red')
    
    plt.title('Mean Timer During Number of Experiments')
    plt.xlabel('Number of Experiments')
    plt.ylabel('Mean Timer')
    plt.legend()
    plt.show()

# Run the simulation and plot the results
run_simulations(100)
