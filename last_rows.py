import random
# descending_boarding.py

from Plane import Plane, plot_results

def run_descending_boarding_simulation(num_experiments=100):
    descending_times = []
    
    for _ in range(num_experiments):
        # Descending Boarding
        plane = Plane()
        plane.generate_passengers()
        plane.descending_boarding()
        descending_times.append(plane.board_passengers())
    
    # Plot results
    plot_results(descending_times, label='Descending Rows', color='green')

# Add descending boarding logic to the Plane class
def descending_boarding(self):
    """Board passengers in descending order of rows, with random seat order in each row."""
    self.passengers.sort(key=lambda p: p.row, reverse=True)
    random.shuffle(self.passengers)

# Monkey patch the Plane class to add descending_boarding
Plane.descending_boarding = descending_boarding

if __name__ == '__main__':
    run_descending_boarding_simulation()
