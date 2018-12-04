# New schedule algorithm for OS managing Accelerator devices

# Need checker for payload > or < allotted
# Hash Map checking for allotted for 
# Track time something gets in OS or GPU
# Track time it would have gotten done
# Track time it got done
# Jobs processed

from enum import Enum
from random import randint
import random

#MACROS
batch_size = 2
cpu_time_multiplier = 2
curr_id = 1


'''
Enum representing job data sizes being passed to GPU or CPU processing
'''
class JobSize(Enum):
    SMALL = 1 
    MEDIUM =2 
    LARGE = 3
    XLARGE = 4

'''
Container Class represent a task. Holds ID and JobSize
'''
class Task:
    '''
    Initializes a Task with a size and a num_Id
    '''
    def __init__(self, num_id, job_size):
        self._size = job_size
        self._num_id = num_id
        self._allocated = 2

    def __str__(self):
        return "Job Size: " + self._size.name \
            + " Num Id: " + str(self._num_id) \
            + " Allocation: " + str(self._allocated)

'''
Takes in a job and puts it in GPU or OS Queue
'''
def assign_queue(task):
    if(task._size is JobSize.SMALL):
        cpu_queue.append(task)
    else:
        gpu_queue.append(task)

'''
Creates 100 random Jobs
'''
def generate_queue():
    queue = []
    for i in range(0,100):
        job_size = randint(1,4)
        global curr_id
        new_task = Task(curr_id, JobSize(job_size))
        queue.append(new_task)
        curr_id += 1
    return queue

'''
Print both queues to the console
'''
def print_queues():
    print("*****GPU Queue*****")
    global gpu_queue
    for task in gpu_queue:
        print(str(task))
    print("*****CPU Queue*****")
    global cpu_queue
    for task in cpu_queue:
        print(str(task))


################
####  Main  ####
################

random.seed(1)

task_queue = generate_queue()
cpu_queue = []
gpu_queue = []


for job in task_queue:
    assign_queue(job)
print("*****Total Tasks*****")
for task in task_queue:
    print(str(task))
print_queues()
