# New schedule algorithm for OS managing Accelerator devices

# Need checker for payload > or < allotted
# Hash Map checking for allotted for 
# Track time something gets in OS or GPU
# Track time it would have gotten done
# Track time it got done
# Jobs processed

from enum import Enum
from random import randint

#MACROS
BATCH_SIZE = 2
CPU_TIME_MULTIPLIER = 2


'''
Enum assigning size of a job
'''
class Job(Enum):
    SMALL = 1 
    MEDIUM =2 
    LARGE = 3
    XLARGE = 4


'''
Creates 100 random Jobs
'''
def generate_queue():
    queue = []
    for i in range(0,100):
        task = randint(1,4)
        queue.append(Job(task))
    return queue

'''
Takes in a job and puts it in GPU or OS Queue
'''
def assign_queue(job):
    if(job.value is 1):
        cpu_queue.append(job)
    else:
        gpu_queue.append(job)
'''
Print both queues to the console
'''
def print_queues():
    print("*****GPU Queue*****")
    print(gpu_queue)
    print("*****CPU Queue*****")
    print(cpu_queue)

task_queue = generate_queue()
cpu_queue = []
gpu_queue = []

for job in task_queue:
    assign_queue(job)
print_queues()

