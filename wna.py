import random
# wna_boarding.py

from Plane import Plane, plot_results

def run_wna_boarding_simulation(num_experiments=100):
    wna_times = []
    
    for _ in range(num_experiments):
        # Window-Middle-Aisle Boarding
        plane = Plane()
        plane.generate_passengers()
        plane.window_middle_aisle_boarding()
        wna_times.append(plane.board_passengers())
    
    # Plot results
    plot_results(wna_times, label='WNA (Window-Middle-Aisle)', color='red')

# Add WNA boarding logic to the Plane class
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

# Monkey patch the Plane class to add window_middle_aisle_boarding
Plane.window_middle_aisle_boarding = window_middle_aisle_boarding

if __name__ == '__main__':
    run_wna_boarding_simulation()
