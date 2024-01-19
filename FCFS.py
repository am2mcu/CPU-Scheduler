import threading

mutex = threading.Lock()

priority_mapping = {'X': 3, 'Y': 2, 'Z': 1}

CPUs = ["Idle", "Idle", "Idle", "Idle"]

ready_queue = []
waiting_queue = []
temp_queue = []

tasks = []
R = []

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

def get_input():
    global R

    r1, r2, r3 = map(int, input().split())
    R = [r1, r2, r3]
    

    num_tasks = int(input())

    for i in range(num_tasks):
        task_name, task_type, duration = input().split()
        tasks.append(Task(task_name, task_type, int(duration)))

def execute(cpu_index):
    global ready_queue

    while True:
        print(f"CPU[{cpu_index}]: {CPUs[cpu_index].name if CPUs[cpu_index] != 'Idle' else 'Idle'}")

        if CPUs[cpu_index] != "Idle":
            CPUs[cpu_index].time_running += 1

            if CPUs[cpu_index].time_running == CPUs[cpu_index].duration:
                if curr_task.type == "X":
                    R[0] += 1
                    R[1] += 1
                elif curr_task.type == "Y":
                    R[1] += 1
                    R[2] += 1
                elif curr_task.type == "Z":
                    R[0] += 1
                    R[2] += 1

                CPUs[cpu_index] = "Idle"
            else:
                continue

        
        if ready_queue == []:
            break


        mutex.acquire()

        curr_task = ready_queue[0]
        if curr_task.type == "X" and R[0] >= 1 and R[1] >= 1:
            CPUs[cpu_index] = ready_queue.pop(0)
        elif curr_task.type == "Y" and R[1] >= 1 and R[2] >= 1:
            CPUs[cpu_index] = ready_queue.pop(0)
        elif curr_task.type == "Z" and R[0] >= 1 and R[2] >= 1:
            CPUs[cpu_index] = ready_queue.pop(0)
        else:
            waiting_queue.append(ready_queue.pop(0))

        mutex.release()

def main():
    global ready_queue

    get_input()

    # sort based on X, Y, Z
    ready_queue = sorted(tasks, key=lambda x: priority_mapping[x.type])

    threads = []
    for i in range(len(CPUs)):
        thread = threading.Thread(target=execute, args=(i,))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()