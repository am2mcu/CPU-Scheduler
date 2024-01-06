import threading
import queue
import time

r1 = threading.Semaphore(1)
r2 = threading.Semaphore(1)
r3 = threading.Semaphore(1)

X, Y, Z = 3, 2, 1

ready_queue = queue.PriorityQueue()
waiting_queue = queue.PriorityQueue()

CPU1 = None
CPU2 = None
CPU3 = None
CPU4 = None

class Task:
    def __init__(self, name, task_type, duration):
        self.name = name
        self.type = task_type
        self.duration = duration
        self.state = "ready"
        self.time_running = 0


def execute_task(task_id, duration):
    print(f"Task {task_id} started")
    time.sleep(duration)
    print(f"Task {task_id} completed")

def shortest_job_first(thread_id, r1, r2, r3, tasks):
    print(f"Thread {thread_id} started")
    while tasks:
        # Sort tasks by duration in ascending order
        tasks = sorted(tasks, key=lambda x: x[2])
        # Get the shortest task
        task_id, task_type, duration = tasks.pop(0)
        # Acquire resources
        r1.acquire()
        r2.acquire()
        r3.acquire()
        # Execute the task
        execute_task(task_id, duration)
        # Release resources
        r1.release()
        r2.release()
        r3.release()
    print(f"Thread {thread_id} completed")

def create_threads(r1, r2, r3, tasks):
    threads = []
    for i in range(4):
        thread = threading.Thread(target=shortest_job_first, args=(i, r1, r2, r3, tasks))
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
        tasks.append((task_name, task_type, int(duration)))

    return r1, r2, r3, tasks

if __name__ == "__main__":
    r1, r2, r3, tasks = get_input()

    main_thread = threading.Thread(target=create_threads, args=(r1, r2, r3, tasks))
    main_thread.start()
    main_thread.join()
