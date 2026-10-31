"""The decision register with staleness alerts, and the generated status block, at Caldwell on day 56."""
from cadence_data import caldwell_register

if __name__ == "__main__":
    print(caldwell_register().status(56))
