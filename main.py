import random
from typing import List, Tuple
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import sys


# Time by which Rita must arrive, in seconds from midnight (9:05 AM).
MEETING_TIME = 9 * 3600 + 5 * 60

# Bus arrival times at Zoo stop (in seconds from midnight)
BUS_SCHEDULE_ZOO = [
    8 * 3600 + 5 * 60,   # 08:05 → 29100 seconds
    8 * 3600 + 16 * 60,  # 08:16 → 29760
    8 * 3600 + 28 * 60,  # 08:28 → 30480
    8 * 3600 + 38 * 60,  # 08:38 → 31140
    8 * 3600 + 48 * 60,  # 08:48 → 31800
    8 * 3600 + 59 * 60   # 08:59 → 32340
]

def format_time(seconds: int) -> str:
    """
    Function that helps format seconds from midnight into hours and minutes for plotting and printing results
    """
    return (datetime(2000, 1, 1) + timedelta(seconds=seconds)).strftime('%H:%M')


def generate_bus_ride_time() -> int:
    """
    Returns how long the bus ride takes, in seconds.
    Typically around 10 minutes, can vary between 8 and 12.
    The typical ride time is based around 10 minutes and 45 seconds,
    to model the fact that bus is realistically a little more likely to be late than early.
    """
    return int(random.triangular(480, 720, 645))

def generate_bus_delay() -> int:
    """
    Returns how long Rita has to wait for the bus in seconds
    """
    return int(random.triangular(0, 120, 0))

def get_next_bus_time(ritas_arrival) -> int | None:
    """
    This function takes as argument Rita's arrival at the zoo station and returns the next available bus time based on bus schedule
    """
    for time in BUS_SCHEDULE_ZOO:
        if ritas_arrival <= time:
            return time
    return None # All busses where missed
    



def simulate_single_journey(departure_time: int) -> bool:
    """
    Simulates a single journey starting at `departure_time` (in seconds from midnight).
    Returns True if Rita is late to her 9:05 AM meeting, False otherwise.
    """

    TO_BUS_STOP = 300  # Fixed time from home to bus stop (5 minutes)
    FROM_BUS_TO_MEETING = 240  # Walk from bus stop to meeting (4 minutes)

    # Arrival at Zoo stop
    rita_arrived_at_zoo = departure_time + TO_BUS_STOP

    # Finding the next scheduled bus
    scheduled_bus_time = get_next_bus_time(rita_arrived_at_zoo)
    if scheduled_bus_time is None:
        return True  # No more buses → Rita is late

    # Waiting time, delay and bus ride time
    wait_for_bus = scheduled_bus_time - rita_arrived_at_zoo
    bus_delay = generate_bus_delay()
    bus_ride_time = generate_bus_ride_time()

    # Total travel time and arrival
    total_time = TO_BUS_STOP + wait_for_bus + bus_delay + bus_ride_time + FROM_BUS_TO_MEETING
    arrival_time = departure_time + total_time

    return arrival_time > MEETING_TIME






def simulations_per_departure(departure_time: int, n: int = 1000) -> float:
    """
    Arguments: departure_time: When exactly Rita exits her house in seconds from midnight,
                n: number of times to run single simulation.
    Runs many simulations over a single departure time.
    Returns the probability of running late as a float based on many runs.
    """
    late_count = 0
    for _ in range(n):
        if simulate_single_journey(departure_time):
            late_count += 1
    return late_count / n
    

def run_simulation_over_range(start_time, end_time, step_minutes, num_simulations) -> List[Tuple[int, float]]:
    """
    Loops over departure times from start_time to end_time in increments of step_minutes.
    For each departure time calls simulation_per_departure function.
    Returns a list of tuples containing each departure times respective simulated probability.
    """
    results = []
    step_seconds = step_minutes * 60

    # Looping over all the provided departure times in 60 second steps
    for departure_time in range(start_time, end_time + 1, step_seconds):
        probability_late = simulations_per_departure(departure_time, num_simulations)
        results.append((departure_time, probability_late))

    return results







def main():
    """
    Main entry point: sets parameters, calls simulation functions,
    outputs and plots results.
    """
    START = 7 * 3600 + 45 * 60   # 07:45
    END = 8 * 3600 + 50 * 60     # 08:50
    STEP = 1                     # every minute
    N_SIMULATIONS = 1000

    results = run_simulation_over_range(START, END, STEP, N_SIMULATIONS)

    for dep_time, prob in results:
        print(f"Departure at {format_time(dep_time)} → Probability of being late: {prob:.2%}")
    
    # Creating seperate lists for departure_times and probabilities using results list of tuples.
    times = [format_time(t[0]) for t in results]
    probs = [t[1] * 100 for t in results]  # * 100 to convert to percentages

    # Creating a plot and generating a file of results.
    plt.figure(figsize=(10, 5))
    plt.plot(times, probs, marker='o')
    plt.title("Probability of Being Late vs. Departure Time")
    plt.xlabel("Departure Time")
    plt.ylabel("Probability of Being Late (%)")
    plt.xticks(ticks=times[::2], rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("late_probabilities.png")  # saves the figure to file
    plt.show()  # shows the figure in a window
    return 0


if __name__ == "__main__":
    sys.exit(main())