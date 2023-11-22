import datetime

import traffic
from traffic.data import opensky
if __name__ == '__main__':
    # Dumb config file
    print(traffic.config_file)
    # Test request that should work
    flight = opensky.history(
        "2017-02-05 15:45",
        stop="2017-02-05 16:45",
        callsign="EZY158T",
        # returns a Flight instead of a Traffic
        return_flight=True
    )
    print(flight)
    assert isinstance(flight, traffic.core.Flight)
