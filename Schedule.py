import random
from enum import Enum
from random import randint

'''
MACROS
'''
# Total CPU quantums
C_TIME = 0
#Used to generate task IDs
CURR_ID = 0
# Total GPU quantums
G_TIME = 0
# Total time when GPU and CPU were running calculations
SAVED_TIME = 0
# Size that a process can be <= to be passed to CPU
SMALL_ENOUGH = 3
# Test Size
TEST_SIZE = 200000

# CPU and GPU queues
cpu_queue = []
gpu_queue = []

###################
###    ENUMS    ###
###################
'''
Enum representing job data sizes being passed to GPU or CPU processing
Currently not really being used, but ._size could be replaced with enums
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

###################
###    CLASS    ###
###################

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
    # End __init__();

    def __str__(self):
        return "Job Size: " + str(self._size) \
            + " Num Id: " + str(self._num_id) \
            + " Allocation: " + str(self._allocated)
    # End __str__();
# End Task Class

###################
###   METHODS   ###
###################

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
    
    # Checks if we are double computing
    if(len(gpu_queue) != 0 and len(cpu_queue) != 0):
        saved = True
    else:
        saved = False

    # Processes one round of GPU
    if(len(gpu_queue) != 0):
        if (gpu_queue[0]._size <= 2):
            task = gpu_queue.pop(0)
            if(task._size == 1):
                G_TIME += 1
            else: 
                G_TIME += 2
        else:
            gpu_queue[0]._size -= 2#gpu_queue[0]._size - 2
            G_TIME +=2

    # Processes one round of CPU
    if(len(cpu_queue) != 0):
        if(cpu_queue[0]._size == 0):
            cpu_queue.pop(0)
            if(saved):
                SAVED_TIME += 1
            else:
                C_TIME += 1
        else:
            cpu_queue[0]._size -= 1#cpu_queue[0]._size - 1
            C_TIME += 1
    return
# End decrement_task_times();

'''
Creates 100 random Jobs
'''
def generate_queue():
    queue = []
    for i in range(0,TEST_SIZE):
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

    #if (task_queue[0]._size <= 1):
    global SMALL_ENOUGH
    if (task_queue[0]._size <= SMALL_ENOUGH):
        if (check_cpu_open()):
            global cpu_queue
            cpu_queue.append(task_queue.pop(0))
        elif (check_gpu_open()):
            global gpu_queue
            gpu_queue.append(task_queue.pop(0))
            '''
        else:
            #task_queue.insert(0, task)'''

    if (task_queue[0]._size > task_queue[0]._allocated):
        task_queue[0]._allocated += 2
        task = task_queue.pop(0)
        task_queue.append(task)
        return
    else:
        if(check_gpu_open()):
            gpu_queue.append(task_queue.pop(0))
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


###################
###    MAIN    ####
###################

'''
Main. Run a Process
'''
def main():
    random.seed(1000)

    #Our Two Processing Avenues
    cpu_queue = []
    gpu_queue = []

    task_queue = generate_queue()


    # This will be main method
    # while len(task_queue) > 0:
    while len(task_queue) != 0:
        GERM_process_task_variant(task_queue)
        decrement_task_times()

    print("Gpu processing time: ", G_TIME)
    print("Cpu processing time: ", C_TIME)
    print("Saved time: ", SAVED_TIME)
    print("Total CPU Jobs: ", (C_TIME + SAVED_TIME) / 2)

# Run main
main()
