import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t

def generate_random_tickets():
    """
    Generates a list of randomly shuffled plane tickets for passengers.
    
    Returns:
        tickets (list): A list of 300 randomly shuffled tickets, each represented 
                        as a list with a row number (1 to 50) and a seat letter ('A' to 'F').
    """
    tickets = []
    rows = range(1, 51)  # Rows from 1 to 50
    seats = ['A', 'B', 'C', 'D', 'E', 'F']  # Seats A to F
    for r in rows:
        for s in seats:
            tickets.append([r, s])
    random.shuffle(tickets)  # Randomize the order of all passengers
    return tickets


def generate_front_to_back_tickets():
    """
    Generates a list of plane tickets where the boarding order is front to back.
    Within each row, the seat order is randomized.
    
    Returns:
        tickets (list): A list of 300 tickets, each represented as a list with a row 
                        number (1 to 50) and a seat letter ('A' to 'F'), boarding front to back.
    """
    rows = range(1, 51)
    seats = ['A', 'B', 'C', 'D', 'E', 'F']
    tickets = []
    for row in rows:
        row_tickets = [[row, seat] for seat in seats]
        random.shuffle(row_tickets)  # Shuffle the seat order within each row
        tickets.extend(row_tickets)  # Add the shuffled row tickets to the main list
    return tickets


def generate_back_to_front_tickets():
    """
    Generates a list of plane tickets where the boarding order is back to front.
    Within each row, the seat order is randomized.
    
    Returns:
        tickets (list): A list of 300 tickets, each represented as a list with a row 
                        number (1 to 50) and a seat letter ('A' to 'F'), boarding back to front.
    """
    rows = range(1, 51)
    seats = ['A', 'B', 'C', 'D', 'E', 'F']
    tickets = []
    for row in rows[::-1]:  # Reverse row order for back-to-front boarding
        row_tickets = [[row, seat] for seat in seats]
        random.shuffle(row_tickets)
        tickets.extend(row_tickets)
    return tickets


def generate_steffen_tickets():
    """
    Generates a list of plane tickets using the Steffen method. 
    This method boards passengers from back to front, alternating by window, middle, 
    and aisle seats to minimize aisle interference.
    
    Returns:
        tickets (list): A list of 300 tickets, ordered according to Steffen's method 
                        (window seats first, then middle, then aisle, from back to front).
    """
    rows = list(range(1, 51))
    tickets = []

    # Board window seats first: A and F
    for seat in ['A', 'F']:
        for row in rows[::-1]:  # From back to front
            tickets.append([row, seat])

    # Then middle seats: B and E
    for seat in ['B', 'E']:
        for row in rows[::-1]:
            tickets.append([row, seat])

    # Finally, aisle seats: C and D
    for seat in ['C', 'D']:
        for row in rows[::-1]:
            tickets.append([row, seat])
    
    return tickets


def run_simulation(method):
    """
    Runs a boarding simulation for a given boarding method.

    Args:
        method (int): An integer representing the boarding method. 
                      1 = Random, 2 = Front-to-Back, 3 = Back-to-Front, 4 = Steffen.

    Returns:
        total_boarding_time (float): The total boarding time for the simulation.
    """
    total_boarding_time = 0
    passengers_list = []

    # Select boarding method
    if method == 1:
        passengers_list = generate_random_tickets()
    elif method == 2:
        passengers_list = generate_front_to_back_tickets()
    elif method == 3:
        passengers_list = generate_back_to_front_tickets()
    elif method == 4:
        passengers_list = generate_steffen_tickets()

    seated_passengers = []
    seated_passengers.append(passengers_list[0])  # First passenger boards
    
    # Process the boarding of subsequent passengers
    for i in range(1, len(passengers_list)):
        cur_pass = passengers_list[i]
        prev_pass = passengers_list[i-1]
        col = cur_pass[1]
        row = cur_pass[0]

        # Simulate different delays based on seat positions
        if row >= prev_pass[0]:  # Boarding a later row
            total_boarding_time += np.random.exponential(5)

        if col == "B" and [row, "C"] in seated_passengers:
            total_boarding_time += np.random.exponential(2)
        if col == "A":
            if [row, "C"] in seated_passengers and [row, "B"] in seated_passengers:
                total_boarding_time += np.random.exponential(3)
            elif [row, "C"] in seated_passengers or [row, "B"] in seated_passengers:
                total_boarding_time += np.random.exponential(2)
        if col == "E" and [row, "D"] in seated_passengers:
            total_boarding_time += np.random.exponential(2)
        if col == "F":
            if [row, "D"] in seated_passengers and [row, "E"] in seated_passengers:
                total_boarding_time += np.random.exponential(3)
            elif [row, "D"] in seated_passengers or [row, "E"] in seated_passengers:
                total_boarding_time += np.random.exponential(2)

        seated_passengers.append(cur_pass)  # Mark passenger as seated
    
    return total_boarding_time


if __name__ == "__main__":
    """
    Runs simulations for all four boarding methods (Random, Front-to-Back, Back-to-Front, Steffen),
    calculates and prints statistical results (mean, standard deviation, confidence intervals),
    and generates a plot comparing the boarding times across multiple experiments.
    """
    num_exp = 100  # Number of experiments to run
    x_vals = [i for i in range(num_exp)]  # X-axis values for the plot
    y_random, y_front_to_back, y_back_to_front, y_steffen = [], [], [], []
    lst_random, lst_front_to_back, lst_back_to_front, lst_steffen = [], [], [], []

    # Run simulations and collect results
    for i in range(1, 101):
        lst_random.append(run_simulation(1))         # Random method simulation
        lst_front_to_back.append(run_simulation(2))  # Front to Back method simulation
        lst_back_to_front.append(run_simulation(3))  # Back to Front method simulation
        lst_steffen.append(run_simulation(4))        # Steffen method simulation

        # Calculate running averages
        y_random.append(sum(lst_random) / i)             # Random
        y_front_to_back.append(sum(lst_front_to_back) / i)  # Front to Back
        y_back_to_front.append(sum(lst_back_to_front) / i)  # Back to Front
        y_steffen.append(sum(lst_steffen) / i)             # Steffen

    # Calculate means
    mean_random = np.mean(lst_random)                   # Random
    mean_front_to_back = np.mean(lst_front_to_back)      # Front to Back
    mean_back_to_front = np.mean(lst_back_to_front)      # Back to Front
    mean_steffen = np.mean(lst_steffen)                  # Steffen

    # Calculate standard deviations
    std_random = np.std(lst_random, ddof=1)              # Random
    std_front_to_back = np.std(lst_front_to_back, ddof=1)  # Front to Back
    std_back_to_front = np.std(lst_back_to_front, ddof=1)  # Back to Front
    std_steffen = np.std(lst_steffen, ddof=1)            # Steffen

    # Calculate standard errors
    std_error_random = std_random / np.sqrt(num_exp)        # Random
    std_error_ftb = std_front_to_back / np.sqrt(num_exp)    # Front to Back
    std_error_btf = std_back_to_front / np.sqrt(num_exp)    # Back to Front
    std_error_steffen = std_steffen / np.sqrt(num_exp)      # Steffen

    # Print results
    print(f"Mean of Random method: {mean_random}")               # Random
    print(f"Mean of Front to Back: {mean_front_to_back}")        # Front to Back
    print(f"Mean of Back to Front: {mean_back_to_front}")        # Back to Front
    print(f"Mean of Steffen method: {mean_steffen}\n")           # Steffen
    
    print(f"STD of Random method: {std_random}")                 # Random
    print(f"STD of Front to Back: {std_front_to_back}")          # Front to Back
    print(f"STD of Back to Front: {std_back_to_front}")          # Back to Front
    print(f"STD of Steffen method: {std_steffen}\n")             # Steffen
    
    print(f"STD error of Random method: {std_error_random}")      # Random
    print(f"STD error of Front to Back: {std_error_ftb}")         # Front to Back
    print(f"STD error of Back to Front: {std_error_btf}")         # Back to Front
    print(f"STD error of Steffen method: {std_error_steffen}\n")  # Steffen

    # Calculate confidence intervals (95% confidence level)
    df = num_exp - 1  # Degrees of freedom
    a1 = 0.05
    critical_value = t.ppf(1 - a1/2, df)  # Two-tailed critical value for t-distribution

    # Margins of error
    random_margin_of_error = critical_value * std_error_random    # Random
    ftb_margin_of_error = critical_value * std_error_ftb          # Front to Back
    btf_margin_of_error = critical_value * std_error_btf          # Back to Front
    steffen_margin_of_error = critical_value * std_error_steffen  # Steffen

    # Print confidence intervals
    print(f"A 95% Confidence Interval for Random method: {(float(mean_random - random_margin_of_error), float(mean_random + random_margin_of_error))}")  # Random
    print(f"A 95% Confidence Interval for Front to Back: {(float(mean_front_to_back - ftb_margin_of_error), float(mean_front_to_back + ftb_margin_of_error))}")  # Front to Back
    print(f"A 95% Confidence Interval for Back to Front: {(float(mean_back_to_front - btf_margin_of_error), float(mean_back_to_front + btf_margin_of_error))}")  # Back to Front
    print(f"A 95% Confidence Interval for Steffen method: {(float(mean_steffen - steffen_margin_of_error), float(mean_steffen + steffen_margin_of_error))}")    # Steffen

    # Plot results
    plt.plot(x_vals, y_random, color="blue", label="Random")              # Random
    plt.plot(x_vals, y_front_to_back, color="orange", label="Front to Back")  # Front to Back
    plt.plot(x_vals, y_back_to_front, color="green", label="Back to Front")  # Back to Front
    plt.plot(x_vals, y_steffen, color="red", label="Steffen")              # Steffen
    plt.xlabel('Number of Experiments')
    plt.ylabel('Mean Time')
    plt.title('Mean Time during Number of Experiments')
    plt.legend(loc='upper right')
    plt.show()
