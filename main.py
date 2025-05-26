import random
from typing import List, Tuple
import matplotlib.pyplot as plt
import sys


# Time by which Rita must arrive, in seconds from midnight (9:05 AM).
MEETING_TIME = 9 * 3600 + 5 * 60

# Bus arrival times at Zoo stop (in seconds from midnight)
BUS_SCHEDULE_ZOO = [
    8 * 3600 + 5 * 60,   # 08:05 → 29100 seconds
    8 * 3600 + 16 * 60,  # 08:16 → 29760
    8 * 3600 + 28 * 60,  # 08:28 → 30480
    8 * 3600 + 38 * 60,  # 08:38 → 31080
    8 * 3600 + 48 * 60,  # 08:48 → 31680
    8 * 3600 + 59 * 60   # 08:59 → 32340
]

def format_time(seconds: int) -> str:
    """Formats seconds from midnight into HH:MM string.

    Args:
        seconds: The time in seconds from midnight.

    Returns:
        A string representation of the time in HH:MM format.

    Raises:
        ValueError: If seconds is negative.
    """
    if seconds < 0:
        raise ValueError("Seconds cannot be negative when formatting time from midnight.")

    hours = (seconds // 3600) 
    minutes = (seconds % 3600) // 60

    return f"{hours:02d}:{minutes:02d}"


def generate_bus_ride_time() -> int:
    """Generates a random bus ride duration.

    The duration is sampled from a triangular distribution.

    :returns: The duration of the bus ride in seconds.
    :rtype: int
    """
    return int(random.triangular(480, 720, 645))


def generate_bus_delay() -> int:
    """Generates a random delay for the bus arrival.

    The delay represents how long Rita has to wait for the bus beyond its
    scheduled arrival, sampled from a triangular distribution.

    :returns: The bus delay time in seconds.
    :rtype: int
    """
    return int(random.triangular(0, 120, 0))


def get_next_bus_time(ritas_arrival) -> int | None:
     """Finds the next available bus time based on Rita's arrival at the zoo station.

    Iterates through the predefined `BUS_SCHEDULE_ZOO` to find the first
    scheduled bus that Rita can catch.

    :param ritas_arrival: Rita's arrival time at the zoo bus stop, in seconds from midnight.
    :type ritas_arrival: int
    :returns: The scheduled time of the next available bus in seconds from midnight,
              or None if all buses on the schedule have already departed before Rita's arrival.
    :rtype: int | None
    """
     for time in BUS_SCHEDULE_ZOO:
         if ritas_arrival <= time:
             return time
     return None # All busses where missed
    

def simulate_single_journey(departure_time: int) -> bool:
    """Simulates a single journey for Rita from her home to the meeting.

    This function calculates Rita's arrival time at the meeting, taking into
    account fixed travel times, bus schedules, and random delays/ride durations.

    :param departure_time: The exact time Rita exits her house, in seconds from midnight.
    :type departure_time: int
    :returns: True if Rita arrives late to her 9:05 AM meeting, False otherwise.
    :rtype: bool
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
     """Runs multiple simulations for a single departure time to estimate lateness probability.

    This function repeatedly calls :func:`simulate_single_journey` for a given
    departure time and calculates the proportion of times Rita is late.

    :param departure_time: The exact time Rita exits her house, in seconds from midnight.
    :type departure_time: int
    :param n: The number of individual journey simulations to run for this departure time.
              Defaults to 1000.
    :type n: int
    :returns: The estimated probability of Rita being late, as a float between 0.0 and 1.0.
    :rtype: float
    """
     late_count = 0
     for _ in range(n):
         if simulate_single_journey(departure_time):
             late_count += 1
     return late_count / n
    

def run_simulation_over_range(start_time: int, end_time: int, step_minutes: int, num_simulations: int) -> List[Tuple[int, float]]:
    """Runs simulations for a range of departure times and collects lateness probabilities.

    This function iterates through a specified time range, calling
    :func:`simulations_per_departure` for each increment to calculate
    the probability of being late.

    :param start_time: The initial departure time for the simulation range, in seconds from midnight.
    :type start_time: int
    :param end_time: The final departure time for the simulation range, in seconds from midnight.
    :type end_time: int
    :param step_minutes: The increment in minutes between each simulated departure time.
    :type step_minutes: int
    :param num_simulations: The number of individual simulations to run for each departure time.
    :type num_simulations: int
    :returns: A list of tuples, where each tuple contains (departure_time, probability_of_being_late).
              Departure times are in seconds from midnight, and probabilities are floats.
    :rtype: List[Tuple[int, float]]
    """
    results = []
    step_seconds = step_minutes * 60

    # Looping over all the provided departure times in 60 second steps
    for departure_time in range(start_time, end_time + 1, step_seconds):
        probability_late = simulations_per_departure(departure_time, num_simulations)
        results.append((departure_time, probability_late))

    return results


def main():
    """Main entry point for the Rita's Bus Journey simulation.

    This function orchestrates the simulation by:
    - Setting up simulation parameters (start/end times, step, number of runs).
    - Calling :func:`run_simulation_over_range` to execute the simulations.
    - Printing the probability of lateness for each departure time.
    - Generating and saving a plot visualizing the results.

    :returns: An exit code, typically 0 for successful execution.
    :rtype: int
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
    plt.xticks(ticks=times[::5], rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("late_probabilities.png")  # saves the figure to file
    return 0


if __name__ == "__main__":
    sys.exit(main())