# Time by which Rita must arrive, in seconds from midnight (9:05 AM).
MEETING_TIME = 9 * 3600 + 5 * 60


def generate_bus_ride_time():
    """
    Returns how long the bus drives in seconds.
    """

def generate_wait_for_bus():
    """
    Returns how long Rita has to wait for the bus in seconds
    """



def simulate_single_journey(departure_time: int, ) -> bool   :
    """
    Simulate a single journey starting at `departure_time`.
    Returns True if Rita is late, False otherwise.
    """
    to_bus_stop = 300   # Seconds
    wait_for_bus = generate_wait_for_bus()  # Seconds
    bus_ride_time = generate_bus_ride_time()    # Seconds
    from_bus_to_meeting = 240   # Seconds

    total_trip_time = to_bus_stop + wait_for_bus + bus_ride_time + from_bus_to_meeting  # Seconds
    arrival_time = departure_time + total_trip_time    # Seconds

    return arrival_time > MEETING_TIME





def simulations_per_departure() -> float:
    """
    Runs many simulations over a single departure time.
    Returns the probability of running late as a float based on many runs.
    """

def run_simulation_over_range(start_time, end_time, step_minutes, num_simulations) -> List[Tuple[time, probability]]:
    """
    Loops over departure times from start_time to end_time in increments of step_minutes.
    For each departure time calls simulation_per_departure function.
    Returns a list of tuples containing each departure times respective simulated probability.
    """







def main():
    """
    Main entry point: sets parameters, calls simulation functions,
    outputs or plots results.
    """








if __name__ == "__main__":
    main()

