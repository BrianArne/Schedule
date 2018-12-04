import random
from enum import Enum
from random import randint

#MACROS
GPU_QUANTUM = 2
CURR_ID = 0
TIME = 0


'''
Enum representing job data sizes being passed to GPU or CPU processing
'''
class JobSize(Enum):
    SMALL = 1 
    MEDIUM =2 
    LARGE = 3
    XLARGE = 4
    XXLarge = 5

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
def assign_two_queue(task):
    if(task._size is JobSize.SMALL):
        cpu_queue.append(task)
    else:
        gpu_queue.append(task)
# End assign_two_queue();

'''
Takes in a job and puts it in GPU queue
Used to for compring algorithm with and without CPU
'''
def assign_one_queue(task):
    gpu_queue.append(task)
# End assign_one_queue();

'''
Creates 100 random Jobs
'''
def generate_queue():
    queue = []
    for i in range(0,100):
        job_size = randint(1,5)
        global CURR_ID
        new_task = Task(CURR_ID, JobSize(job_size))
        queue.append(new_task)
        CURR_ID += 1
    return queue
# End generate_queue();

'''
Looks at next task and assigns processor depending on JobSize and Allocated Time
While also implementing a GERM scheduling policy
'''
def GERM_process_task_variant(task_queue):
    task = task_queue.pop(0)
    if task._size == JobSize.SMALL:
        global cpu_queue
        cpu_queue.append(task)
        return
    if task._size.value > task._allocated:
        task._allocated += 2
        task_queue.append(task)
        return
    else:
        global gpu_queue
        gpu_queue.append(task)
    return
# End process_task();

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
# End print_queues();

################
####  Main  ####
################

random.seed(1)

task_queue = generate_queue()
print(len(task_queue))
cpu_queue = []
gpu_queue = []

while len(task_queue) > 0:
    print(len(task_queue))
    GERM_process_task_variant(task_queue)
print_queues()
print(len(cpu_queue))
print(len(gpu_queue))
'''Comments
New schedule algorithm for OS managing Accelerator devices

Need checker for payload > or < allotted
Track time something gets in OS or GPU
Track time it would have gotten done
Track time it got done
Jobs processed
'''
