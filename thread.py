import threading
import queue
import time

resources = [threading.Semaphore(), threading.Semaphore(), threading.Semaphore()]

X, Y, Z = 3, 2, 1

ready_queue = queue.PriorityQueue()
waiting_queue = queue.PriorityQueue()

CPU1 = "Idle"
CPU2 = "Idle"
CPU3 = "Idle"
CPU4 = "Idle"

class Task:
    def __init__(self, name, task_type, duration):
        self.name = name
        self.type = task_type
        self.duration = duration
        self.state = "ready"
        self.time_running = 0
    
    def change_state(self, state):
        self.state = state
    
    def update_time(self, time):
        self.time_running += time


def execute_task(task_id, duration):
    print(f"Task {task_id} started")
    time.sleep(duration)
    print(f"Task {task_id} completed")

    while tasks:
        if task_type == "X":
            r1.acquire()
            r2.acquire()
            queue_X.put((task_duration, task_name))
        elif task_type == "Y":
            r2.acquire()
            r3.acquire()
            queue_Y.put((task_duration, task_name))
        elif task_type == "Z":
            r1.acquire()
            r3.acquire()
            queue_Z.put((task_duration, task_name))


def shortest_job_first(tasks):
    # while tasks:
        # Sort tasks by duration in ascending order
    tasks = sorted(tasks, key=lambda x: x[2])
    #     # Get the shortest task
    #     task_id, task_type, duration = tasks.pop(0)
    #     # Acquire resources
    #     r1.acquire()
    #     r2.acquire()
    #     r3.acquire()
    #     # Execute the task
    #     execute_task(task_id, duration)
    #     # Release resources
    #     r1.release()
    #     r2.release()
    #     r3.release()
    # print(f"Thread {thread_id} completed")

def create_threads(r1, r2, r3, tasks):
    resources[0] = threading.Semaphore(r1)
    resources[1] = threading.Semaphore(r2)
    resources[2] = threading.Semaphore(r3)
    shortest_job_first(tasks)

    threads = []
    for i in range(4):
        thread = threading.Thread(target=execute_task)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def get_input():
    r1, r2, r3 = map(int, input("Enter the number of R1, R2, R3 resources separated by space: ").split())

    num_tasks = int(input("Enter the number of tasks: "))

    tasks = []
    for i in range(num_tasks):
        task_name, task_type, duration = input(f"Enter the name, type, and duration of task {i+1} separated by space: ").split()
        tasks.append(Task(task_name, task_type, int(duration)))

    return r1, r2, r3, tasks

if __name__ == "__main__":
    r1, r2, r3, tasks = get_input()

    main_thread = threading.Thread(target=create_threads, args=(r1, r2, r3, tasks))
    main_thread.start()
    main_thread.join()
