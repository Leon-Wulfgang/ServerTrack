
0. Flask microFramework was used, to install:
    `pip install Flask`
    > if you have difficulty installing Flask this way, please use the Flask-0.11.tar.gz package to install from the source code.

1. to start the API server for ServerTrack: (keep it running when doing requests to it)
    `python servertrack.py`

2. to run tests: (the results will be displayed in readable JSON format in the terminal)
    `python tester.py`

Test cases/functions in tester.py
    0. CONFIGS section defines constants for tester
    1. Populate server data using POST with timestamp for the past X hours
    2. run POSTs continuously for X seconds to populate recent data
    3. GET the cpu/ram status for the last 60 minutes broken down by minute
    4. GET the cpu/ram status for the last 24 hours broken down by hour

problem description
-

This specific challenge is called ServerTrack and allows you to demonstrate how you might implement a basic server monitoring system.  
   
In this project, two web API endpoints are necessary. They are:  
   
1. Record load for a given server  
This should take a:  
                • server name (string)  
                • CPU load (double)  
                • RAM load (double)  
And apply the values to an in-memory model used to provide the data in endpoint #2.  
   
2. Display loads for a given server  
This should return data (if it has any) for the given server:  
                • A list of the average load values for the last 60 minutes broken down by minute  
                • A list of the average load values for the last 24 hours broken down by hour  
   
Assume these endpoints will be under a continuous load being called for thousands of individual servers every minute.  
   
There is no need to persist the results to any permanent storage, just keep the data in memory to keep things simple.  
