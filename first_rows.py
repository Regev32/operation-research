import random
# ascending_boarding.py

from Plane import Plane, plot_results

def run_ascending_boarding_simulation(num_experiments=100):
    ascending_times = []
    
    for _ in range(num_experiments):
        # Ascending Boarding
        plane = Plane()
        plane.generate_passengers()
        plane.ascending_boarding()
        ascending_times.append(plane.board_passengers())
    
    # Plot results
    plot_results(ascending_times, label='Ascending Rows', color='orange')

# Add ascending boarding logic to the Plane class
def ascending_boarding(self):
    """Board passengers in ascending order of rows, with random seat order in each row."""
    self.passengers.sort(key=lambda p: p.row)
    random.shuffle(self.passengers)

# Monkey patch the Plane class to add ascending_boarding
Plane.ascending_boarding = ascending_boarding

if __name__ == '__main__':
    run_ascending_boarding_simulation()
