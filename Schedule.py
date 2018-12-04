import random
from enum import Enum
from random import randint

#MACROS
GPU_QUANTUM = 2
CURR_ID = 0
G_TIME = 0
C_TIME = 0
SAVED_TIME = 0


'''
Enum representing job data sizes being passed to GPU or CPU processing
'''
class JobSize(Enum):
    HALF_SMALL = 0
    SMALL = 1 
    MEDIUM =2 
    LARGE = 3
    XLARGE = 4
    XXLarge = 5
    
    '''
    Overwritting subtraction method to subtract int from value
    '''
    def __sub__(self, y):
        self.value = self.value - 1
    # End __sub__();

# End JobSize Enum

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
        return "Job Size: " + str(self._size) \
            + " Num Id: " + str(self._num_id) \
            + " Allocation: " + str(self._allocated)
# End Task Class

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
Returns bool. Checks if cpu can take another task
'''
def check_cpu_open():
    global cpu_queue
    if len(cpu_queue) == 0:
        return True
# End check_cpu_open();

'''
Returns bool. Checks if gpu can take another task
'''
def check_gpu_open():
    global gpu_queue
    if len(gpu_queue) == 0:
        return True
# End check_gpu_open();

'''
Looks at each process and "processes them"
Adds quantum time to overall time
'''
def decrement_task_times():
    global gpu_queue
    global cpu_queue
    global G_TIME
    global C_TIME
    global SAVED_TIME
    
    gpu_flag = True

    if(len(gpu_queue) != 0):
        if (gpu_queue[0]._size <= 2):
            task = gpu_queue.pop(0)
            if(task._size == 1):
                G_TIME += 1
            else: 
                G_TIME += 2
        else:
            gpu_queue[0]._size = gpu_queue[0]._size - 2
    if(len(gpu_queue) == 0):
        gpu_flag = False

    if(len(cpu_queue) != 0):
        if(cpu_queue[0]._size == 0):
            cpu_queue.pop(0)
            if(gpu_flag):
                SAVED_TIME += 1
            else:
                C_TIME += 1
        else:
            cpu_queue[0]._size = cpu_queue[0]._size - 1
    return
# End decrement_task_times();

'''
Creates 100 random Jobs
'''
def generate_queue():
    queue = []
    for i in range(0,100):
        job_size = randint(1,5)
        global CURR_ID
        new_task = Task(CURR_ID, job_size)
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
    
    if (task._size == 1):
        if (check_cpu_open()):
            global cpu_queue
            cpu_queue.append(task)
        elif (check_gpu_open()):
            global gpu_queue
            gpu_queue.append(task)
        else:
            task_queue.insert(0, task)
        return

    if task._size > task._allocated:
        task._allocated += 2
        task_queue.append(task)
        return
    else:
        if(check_gpu_open()):
            gpu_queue.append(task)
        else:
            task_queue.insert(0,task)
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
cpu_queue = []
gpu_queue = []

task_queue = generate_queue()
'''
for task in task_queue:
    assign_two_queue(task)
'''


# This will be main method
while len(task_queue) > 0:
    GERM_process_task_variant(task_queue)
    decrement_task_times()

print("G_TIME: ", G_TIME)
print("C_TIME: ", C_TIME)
print("SAVED_TIME: ", SAVED_TIME)

'''Comments
New schedule algorithm for OS managing Accelerator devices

Need checker for payload > or < allotted
Track time something gets in OS or GPU
Track time it would have gotten done
Track time it got done
Jobs processed
'''
