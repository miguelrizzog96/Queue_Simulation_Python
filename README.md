# Discrete Event simulation of a single server queue using Python. 
*Written by: Miguel Angel Rizzo Gonzalez*
![](https://user-images.githubusercontent.com/69512046/93006624-747df780-f52c-11ea-9b3a-8e0f97714b87.jpg)


## Why Study Queues?
**Waiting to be attended is part of daily life. We wait in restaurants, we do a
line to board a plane, and we stand in line to be served at
official dependencies. The phenomenon of waiting is not limited to human beings:
jobs wait to be processed, planes fly in circles at different heights
until they are allowed to land, and the cars stop at traffic lights. Deleting the
waiting entirely is not a feasible option because the cost of installation and
operation of the operation center can be prohibitive. Our only recourse is to search
the balance between the cost of offering a service and the cost of waiting for it to be served.
Queue analysis is the vehicle to achieve this goal.** *(Taha,H.)* 
##  Objective: 
- ***Generate a Simulation model that outputs the performance measures, such as average length, average waiting time, utilization of the system, etc. to provide information for designing or improving service facilities.***

## Necessary data
- λ: the arrival rate (the expected time between each customer arriving, e.g. 1 minute)
- μ: the service rate (the expected service time, e.g. 1.5 minutes)
- the distribution of the data
- c: the number of servers
- The number of customers to be simulated

## Data Visualization

Here are the distributions of the data and the value counts for other variables like occupation and number of customers in the system. Below are a few key points of the model.


![](https://user-images.githubusercontent.com/69512046/93101315-1b22df00-f678-11ea-91f7-b1b2a4b08e7b.png)
![](https://user-images.githubusercontent.com/69512046/93101333-1f4efc80-f678-11ea-9b21-e1a16462497e.png)
![](https://user-images.githubusercontent.com/69512046/93101325-1ceca280-f678-11ea-8315-9ec5cde3b81a.png)
![](https://user-images.githubusercontent.com/69512046/93101302-18c08500-f678-11ea-9729-c573d85f666e.png)
![](https://user-images.githubusercontent.com/69512046/93101287-16f6c180-f678-11ea-9265-5b5804c180d5.png)

## Model Development Steps
Using Python 3.7.6

- Generated arrival and service times with random number generation using the python library `numpy`
- Generated lists and dataframes with conditional statements to represent the events ocurring in the queue
- Used the generated model for simulating a Single server queue with 1000 customers

## Results

|  Output:                 |          | 
| ----------- | ----------- |
|  Time Between Arrivals:  | 0.2558   |
| Service Time:            |  0.1580  |        
| Utilization:             |  0.367   |
|  Expected wait time in line:|   0.22732 |  
|  Expected number of customers in line:|   1.0005 |  
|   Expected number of clients in the system: |  1.49825 |  
|   Expected time spent on the system:|   0.38538 |  

	#[Source Code](https://github.com/miguelrizzog96/Simulation-of-a-single-server-queue/blob/master/QueuingSimulation.py)
