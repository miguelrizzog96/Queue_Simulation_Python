import simpy
import random


def customer(env, name, washing_machines, driers, wash_time_range, dry_time_range, leave_probability,
              leave_probability_full,
             queue_lengths,driers_queue_lengths , washing_machines_queue_lengths,
             time_in_systems, utilization_washers, 
             utilization_driers, timeline,dry_only):
  
    arrival_time = env.now
    timeline.append(f"{name} arrives at the laundromat at {arrival_time:.2f}")
    
    if random.random() < dry_only:
        # Check if both washing machines and driers are available
        if washing_machines.count == washing_machines.capacity:
            if random.random() < leave_probability_full:
                timeline.append(f"{name} leaves the laundromat due to full washing machine capacity at {env.now:.2f}")
                return
        with washing_machines.request() as wash_request:
            yield wash_request
            start_wash_time = env.now
            timeline.append(f"{name} starts using a washing machine at {start_wash_time:.2f}")
            wash_time = random.uniform(*wash_time_range)
            yield env.timeout(wash_time)
            end_wash_time = env.now
            timeline.append(f"{name} finishes washing at {end_wash_time:.2f}")
            wash_count.append(1)

            # Check if the customer leaves after washing
            if random.random() < leave_probability:
                timeline.append(f"{name} leaves the laundromat after washing at {end_wash_time:.2f}")
                return
    if driers.count == driers.capacity:
        if random.random() < leave_probability_full:
            timeline.append(f"{name} leaves the laundromat due to full driers capacity at {env.now:.2f}")
            return
        # Check if the customer uses a drier
    
    with driers.request() as dry_request:
        yield dry_request
        start_dry_time = env.now
        timeline.append(f"{name} starts using a drier at {start_dry_time:.2f}")
        dry_time = random.uniform(*dry_time_range)
        yield env.timeout(dry_time)
        end_dry_time = env.now
        timeline.append(f"{name} finishes drying at {end_dry_time:.2f}")
        drier_count.append(1)

    leave_time = env.now
    timeline.append(f"{name} leaves the laundromat at {leave_time:.2f}")

    # Update metrics
    queue_lengths.append(len(washing_machines.queue) + len(driers.queue))
    driers_queue_lengths.append( len(driers.queue))
    washing_machines_queue_lengths.append(len(washing_machines.queue))
    time_in_systems.append(leave_time - arrival_time)
    utilization_washers.append(washing_machines.count / washing_machines.capacity)
    utilization_driers.append(driers.count / driers.capacity)

def customer_generator(env, washing_machines, driers, arrival_rate, wash_time_range,
                       dry_time_range, leave_probability, leave_probability_full,
                       queue_lengths,driers_queue_lengths, washing_machines_queue_lengths,
                       time_in_systems, utilization_washers, utilization_driers,timeline,dry_only):
    customer_count = 0
    while True:
        yield env.timeout(random.expovariate(arrival_rate))
        customer_count += 1
        env.process(customer(env, f"Customer-{customer_count}", washing_machines, driers, wash_time_range,
                             dry_time_range, leave_probability,  leave_probability_full,
                             queue_lengths,driers_queue_lengths, washing_machines_queue_lengths,
                             time_in_systems, utilization_washers, utilization_driers,timeline,dry_only))

# Simulation setup
env = simpy.Environment()
washing_machines = simpy.Resource(env, capacity=3)
driers = simpy.Resource(env, capacity=2)
dry_only=0.9

# Metrics
timeline= []
queue_lengths = []
driers_queue_lengths = []
washing_machines_queue_lengths = []
time_in_systems = []
utilization_washers = []
utilization_driers = []
wash_count = []
drier_count = []

# Start the simulation
env.process(customer_generator(env, washing_machines, driers, arrival_rate=0.025, wash_time_range=(35, 45), dry_time_range=(15, 30),
                               leave_probability=0.1, leave_probability_full=0.5,
                               queue_lengths=queue_lengths,washing_machines_queue_lengths =washing_machines_queue_lengths,
                               driers_queue_lengths =driers_queue_lengths,
                               time_in_systems=time_in_systems,
                               utilization_washers=utilization_washers, 
                               utilization_driers=utilization_driers, timeline=timeline,dry_only=dry_only))

env.run(until=870)#minutes870

# Calculate and print metrics
avg_queue_washing_machine= sum(washing_machines_queue_lengths)/len(washing_machines_queue_lengths)
avg_queue_drier= sum(driers_queue_lengths)/len(driers_queue_lengths)
avg_queue_length = sum(queue_lengths) / len(queue_lengths)
avg_time_in_system = sum(time_in_systems) / len(time_in_systems)
avg_utilization_washers = sum(utilization_washers) / len(utilization_washers)
avg_utilization_driers = sum(utilization_driers) / len(utilization_driers)
total_wash_count = sum(wash_count)
total_drier_count = sum(drier_count)
earnings= sum(drier_count)*3 + sum(wash_count)*4


print(f"Average Drier queue: {avg_queue_drier:.2f}")
print(f"Average Washing Machine Queue: {avg_queue_washing_machine:.2f}")
print(f"Average # of People waiting in the system: {avg_queue_length:.2f}")
print(f"Average Time in System: {avg_time_in_system:.2f}")
print(f"Average Utilization of Washers: {avg_utilization_washers:.2%}")
print(f"Average Utilization of Driers: {avg_utilization_driers:.2%}")
print(f"Total Washing Machine Usage: {total_wash_count}")
print(f"Total Drier Usage: {total_drier_count}")
print(f"Earnings: {earnings}")


