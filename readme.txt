
0. Flask microFramework was used, to install:
    pip install Flask
    # if you have difficulty installing Flask this way, please use the Flask-0.11.tar.gz package to install from the source code.

1. to start the API server for ServerTrack: (keep it running when doing requests to it)
    python servertrack.py

2. to run tests: (the results will be displayed in readable JSON format in the terminal)
    python tester.py

Test cases/functions in tester.py
    0. CONFIGS section defines constants for tester
    1. Populate server data using POST with timestamp for the past X hours
    2. run POSTs continuously for X seconds to populate recent data
    3. GET the cpu/ram status for the last 60 minutes broken down by minute
    4. GET the cpu/ram status for the last 24 hours broken down by hour


