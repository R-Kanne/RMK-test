# RMK-test

## General Approach

The goal of this project is to estimate the probability that Rita will be late to her 9:05 AM meeting, depending on the time she leaves her home, given that she takes bus number 8 from Zoo to Toompark in Tallinn.

My approach involves building a simulation model that incorporates key timing variables and randomness to realistically reflect the variability in bus arrival and travel times. Specifically:

- **Main simulation function:** A central function will combine randomized datapoints to simulate a single trial of Rita’s journey from home to the meeting. This function will include the most important factors that affect Rita’s arrival time and lateness.

- **Multiple runs and aggregation:** By running this simulation repeatedly (e.g., thousands of times) with the same input parameters, I will collect a distribution of possible arrival times. From this, I can calculate the empirical probability of Rita being late for each departure time.

- **Output and visualization:** The simulation results will be saved in a structured format suitable for further analysis and visualization, such as plotting lateness probability curves depending on the departure time.


---

