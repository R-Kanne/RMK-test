import pytest
from main import format_time, get_next_bus_time, BUS_SCHEDULE_ZOO, simulate_single_journey

def test_format_time():
    # Basic cases
    assert format_time(0) == "00:00"
    assert format_time(1) == "00:00"  # Smallest non-zero
    assert format_time(59) == "00:00"  # Just under a minute

    # Test cases around 1 minute
    assert format_time(1 * 60) == "00:01"  # Exactly one minute
    assert format_time(1 * 60 + 1) == "00:01"  # Just over one minute

    # Test cases around 1 hour
    assert format_time(1 * 3600) == "01:00"  # Exactly one hour
    assert format_time(1 * 3600 - 1) == "00:59" # Just under one hour
    assert format_time(1 * 3600 + 1) == "01:00" # Just over one hour

    # Test cases for exact hours
    assert format_time(2 * 3600) == "02:00"  # Exactly two hours
    assert format_time(15 * 3600) == "15:00" # Exactly fifteen hours

    # Test cases for hours and minutes combinations
    assert format_time(1 * 3600 + 1 * 60) == "01:01"  # One hour and one minute
    assert format_time(15 * 3600 + 5 * 60 + 21) == "15:05" # 15 hours, 5 minutes, 21 seconds (54321 seconds)
    assert format_time(23 * 3600 + 59 * 60 + 59) == "23:59" # The maximum valid time before 24 hours

    # Test cases for negative seconds (expecting ValueError)
    with pytest.raises(ValueError):
        format_time(-1)
    with pytest.raises(ValueError):
        format_time(-100)


def test_get_next_bus_time():
    # Test cases for early arrivals before the first bus
    assert get_next_bus_time(0 * 3600 + 0 * 60) == BUS_SCHEDULE_ZOO[0]  # Rita arrives 00:00
    assert get_next_bus_time(8 * 3600 + 0 * 60) == BUS_SCHEDULE_ZOO[0]  # Rita arrives 08:00 (before first bus)

    # Test cases for arriving exactly at a bus time
    assert get_next_bus_time(8 * 3600 + 5 * 60) == BUS_SCHEDULE_ZOO[0]   # Rita arrives 08:05:00 (first bus)
    assert get_next_bus_time(8 * 3600 + 16 * 60) == BUS_SCHEDULE_ZOO[1]  # Rita arrives 08:16:00 (second bus)
    assert get_next_bus_time(8 * 3600 + 28 * 60) == BUS_SCHEDULE_ZOO[2]  # Rita arrives 08:28:00 (third bus)
    assert get_next_bus_time(8 * 3600 + 38 * 60) == BUS_SCHEDULE_ZOO[3]  # Rita arrives 08:38:00 (fourth bus)
    assert get_next_bus_time(8 * 3600 + 48 * 60) == BUS_SCHEDULE_ZOO[4]  # Rita arrives 08:48:00 (fifth bus)
    assert get_next_bus_time(8 * 3600 + 59 * 60) == BUS_SCHEDULE_ZOO[5]  # Rita arrives 08:59:00 (last bus)

    # Test cases for arriving just before a bus (should catch that bus)
    assert get_next_bus_time(8 * 3600 + 15 * 60 + 59) == BUS_SCHEDULE_ZOO[1]  # Rita arrives 08:15:59 (just before second bus)
    assert get_next_bus_time(8 * 3600 + 27 * 60 + 59) == BUS_SCHEDULE_ZOO[2]  # Rita arrives 08:27:59 (just before third bus)
    assert get_next_bus_time(8 * 3600 + 58 * 60 + 59) == BUS_SCHEDULE_ZOO[5]  # Rita arrives 08:58:59 (just before last bus)

    # Test cases for arriving just after a bus departs (should catch the next one)
    assert get_next_bus_time(8 * 3600 + 5 * 60 + 1) == BUS_SCHEDULE_ZOO[1]   # Rita arrives 08:05:01 (missed 08:05, gets 08:16)
    assert get_next_bus_time(8 * 3600 + 16 * 60 + 1) == BUS_SCHEDULE_ZOO[2]  # Rita arrives 08:16:01 (missed 08:16, gets 08:28)
    assert get_next_bus_time(8 * 3600 + 28 * 60 + 1) == BUS_SCHEDULE_ZOO[3]  # Rita arrives 08:28:01 (missed 08:28, gets 08:38)
    assert get_next_bus_time(8 * 3600 + 38 * 60 + 1) == BUS_SCHEDULE_ZOO[4]  # Rita arrives 08:38:01 (missed 08:38, gets 08:48)
    assert get_next_bus_time(8 * 3600 + 48 * 60 + 1) == BUS_SCHEDULE_ZOO[5]  # Rita arrives 08:48:01 (missed 08:48, gets 08:59)

    # Test cases for arriving after all buses have departed (should return None)
    assert get_next_bus_time(8 * 3600 + 59 * 60 + 1) is None  # Rita arrives 08:59:01 (missed last bus)
    assert get_next_bus_time(9 * 3600 + 30 * 60) is None     # Rita arrives 09:30:00 (much later)
    assert get_next_bus_time(10 * 3600 + 0 * 60) is None     # Rita arrives 10:00:00 (even later)