# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 14:00:13 2020

@author: Miguel Rizzo
"""

##single server 
#
#
#
#
#
#Importing Libraries
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


# Single server, single queue simulation parameters
l = 4 # average number of arrivals per minute
µ = 6 # average number of people served per minute
ncust = 1000 # number of customers
c=1 # number of servers

 # generating inter arrival times using exponential distribution
   
inter_arrival_times = list(np.random.exponential(scale=1/l,size=ncust))

    
arrival_times= []# list of arrival times of a person joining the queue
service_times = [] # list of service times once they reach the front
finish_times = [] # list of finish times after waiting and being served
    
arrival_times = [0 for i in range(ncust)]
finish_times = [0 for i in range(ncust)]
    
arrival_times[0]=round(inter_arrival_times[0],4)#arrival of first customer
    
    #Generate arrival times
for i in range(1,ncust):
    arrival_times[i]=round((arrival_times[i-1]+inter_arrival_times[i]),2)
    
        
    # Generate random service times for each customer 
service_times = list(np.random.exponential(scale=1/µ,size=ncust))

        
    #finish time for first customer
finish_times[0]=round((arrival_times[0]+service_times[0]),2)
    
    #generating finish times
for i in range(1,ncust):
    finish_times[i] = round((max(arrival_times[i], finish_times[i-1]) + service_times[i]),2)
 
        # Total time spent in the system by each customer
total_times =[abs(round((finish_times[i]-arrival_times[i]),2)) for i in range(ncust)]



     # Time spent@waiting before being served (time spent in the queue)
wait_times = [abs(round((total_times[i] - service_times[i]),2)) for i in range(ncust)]
 

    #creating a dataframe with all the data of the model
data = pd.DataFrame(list(zip(arrival_times,service_times,total_times,finish_times,wait_times,inter_arrival_times)), 
               columns =['arrival_times', 'service_times','total_times','finish_times','wait_times','inter_arrival_times']) 

#generating time between events , and their description (arrivals, departures)

tbe=list([0])
timeline=['simulation starts']
for i in range(1,ncust):
    tbe.append(data['arrival_times'][i])
    tbe.append(data['finish_times'][i])
    timeline.append('customer ' +str(i)+' arrived')
    timeline.append('customer ' +str(i)+' left')
    
timeline.append('simulation ends')
tbe.append(data.finish_times.max())


timeline = pd.DataFrame(list(zip(tbe,timeline)), 
               columns =['TBE','Timeline']).sort_values(by='TBE').reset_index()
timeline=timeline.drop(columns='index')

#generating the number of customers inside the system at any given time of the simulation

timeline['n']=0
x=0

for i in range(1,2*ncust):
    if len(((timeline.Timeline[i]).split()))>2:
        z=str(timeline['Timeline'][i]).split()[2]
    else:
        continue
    if z =='arrived':
        x = x+1
        timeline['n'][i]=x
    else:
        x=x-1
        if x==-1:
            x=0
        timeline['n'][i]=x

data['occupied']=[0 for i in range(ncust)]
for i in range(1,ncust):
    
    if data.arrival_times[i]>data.finish_times[i-1]:
        data['occupied'][i]=1
    else:
        data['occupied'][i]=0
    
    
#checking central tendency measures and dispersion of the data
timeline.n.describe()
data.occupied.value_counts()

timeline['Lq']=0
for i in timeline.index:
    if timeline.n[i]>1:
        timeline.Lq[i]= timeline['n'][i]-c

#plots

plt.figure(figsize=(12,4))
sns.lineplot(x=data.index,y=wait_times,color='black')
plt.xlabel('Customer number')
plt.ylabel('minutes')
plt.title('Wait time of customers')
sns.despine()
plt.show()

plt.figure(figsize=(7,7))
sns.distplot(inter_arrival_times,kde=False,color='r')
plt.title('Time between Arrivals')
plt.xlabel('Minutes')
plt.ylabel('Frequency')
sns.despine()
plt.show()

plt.figure(figsize=(8,8))
sns.distplot(service_times,kde=False)
plt.title('Service Times')
plt.xlabel('Minutes')
plt.ylabel('Frequency')
sns.despine()
plt.show()

plt.figure(figsize=(8,8))
sns.distplot(timeline.n,kde=False,color='g')
plt.title('Number of customers in the system')
plt.xlabel('n')
plt.ylabel('Frequency')
sns.despine()
plt.show()


plt.figure(figsize=(7,7))
sns.countplot(data.occupied,color='mediumpurple')
plt.title('Utilization')
plt.xlabel('occupied')
sns.despine()
plt.show()


timeline.n.value_counts()/timeline.n.shape[0]

print('Output:','\n',
      'Time Between Arrivals: ',str(data.inter_arrival_times.mean()),'\n',
      'Service Time: ',str(data.service_times.mean()),'\n'
      ' Utilization: ',str(data.occupied.mean()),'\n',
      'Expected wait time in line:',str(data['wait_times'].mean()),'\n',
       'Expected number of customers in line:',str(timeline['Lq'].mean()/2),'\n',
       'Expected number of clients in the system:',str(timeline['n'].mean()/2),'\n'
      ' Expected time spent on the system:',str(data.total_times.mean()),'\n',)
