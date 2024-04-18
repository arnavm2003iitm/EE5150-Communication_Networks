import numpy as np
import matplotlib.pyplot as plt
from numpy import random
import statistics
import csv
import pandas as pd

scheme = 'lifo'

time_steps = 10000

lmbda_lst = np.array(range(1, 10)) # 1/mean inter-arrival times
mu = 10 # 1/mean service time

queue = [] # each element stores the total time spent in the queue
queue_len = []
wait_time = []

mean_wait_time = []
mean_queue_len = []

offered_load = []

print("--LIFO M/M/1 Queue Simulation--")

for lmbda in lmbda_lst:

    num_arrivals = [] # list to store the number of arrivals in the time slot
    num_services = [] # list to store the number of services in the time slot 

    for t in range(0, time_steps):

        num_arrivals.append(random.poisson(lam=lmbda)) # number of arrivals occuring in the time slot
        num_services.append(int(random.exponential(scale=mu))) # number of services in the time slot

        queue_len.append(len(queue))
        queue = [(queue[i]+1) for i in range(0, len(queue))] 

        for i in range(num_arrivals[t]): # add arrivals to the end of the queue
            queue.append(0)
        
        # print(queue)

        for i in range(num_services[t]): # remove the required number of elements from end of the queue
            try:
                wait_time.append(queue.pop())
            except:
                pass
        
        # print(queue)

    avg_queue_len = statistics.mean(queue_len)
    avg_wait_time = statistics.mean(wait_time)

    mean_wait_time.append(avg_wait_time)
    mean_queue_len.append(avg_queue_len)

    offered_load.append(lmbda/mu)

    print("Simulation for lambda = ", lmbda)
    print("--Simulation Statistics--")
    print("Average Queue Length: ", avg_queue_len)
    print("Average Wait Time: ", avg_wait_time)
    print("Offered Load to the System: ", offered_load[lmbda-1])
    print()

directory_data_lst = [lmbda_lst, [mu]*9, offered_load, mean_queue_len, mean_wait_time]
directory_data = list(zip(*directory_data_lst))
print(pd.DataFrame(directory_data).to_string())

with open(('simulation_data_{}.csv'.format(scheme)), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(directory_data)

plt.plot(offered_load, mean_queue_len)
plt.xlabel('Offered Load ($\lambda/\mu$)')
plt.ylabel('Mean queue length')
plt.title('Plot of Mean Queue Length vs. Offered Load to System')
plt.grid()
plt.savefig('mean_queue_len_{}'.format(scheme))
plt.show()


plt.plot(offered_load, mean_wait_time)
plt.xlabel('Offered Load ($\lambda/\mu$)')
plt.ylabel('Mean waiting time')
plt.title('Plot of Mean Waiting Time vs. Offered Load to System')
plt.grid()
plt.savefig('mean_wait_time_{}'.format(scheme))
plt.show()