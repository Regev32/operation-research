# Plane.py

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
    
    def is_left_side(self, seat):
        """Check if the seat is on the left side of the aisle (A, B, C)."""
        return seat in ['A', 'B', 'C']

    def is_right_side(self, seat):
        """Check if the seat is on the right side of the aisle (D, E, F)."""
        return seat in ['D', 'E', 'F']

    def board_passengers(self):
        """Simulates the boarding process for all passengers."""
        total_boarding_time = 0
        self.seated_passengers = set()  # Reset seated passengers each time
        
        for passenger in self.passengers:
            # Determine if the current passenger is on the left or right side of the aisle
            if self.is_left_side(passenger.seat):
                # Check if there are any blocking passengers on the left side of the aisle (A, B, C)
                blocking_passengers = sum(
                    1 for p in self.seated_passengers 
                    if p.row == passenger.row and self.is_left_side(p.seat) and p.seat < passenger.seat
                )
            elif self.is_right_side(passenger.seat):
                # Check if there are any blocking passengers on the right side of the aisle (D, E, F)
                blocking_passengers = sum(
                    1 for p in self.seated_passengers 
                    if p.row == passenger.row and self.is_right_side(p.seat) and p.seat < passenger.seat
                )
            
            passenger.blocking_passengers = blocking_passengers
            
            # The passenger settles in their seat
            time_to_seat = passenger.settle_in_seat()
            total_boarding_time += time_to_seat
            
            # Mark this passenger as seated
            self.seated_passengers.add(passenger)
        
        return total_boarding_time

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
