import threading
import time

semaphore = threading.Semaphore()
semaphore_out = threading.Semaphore(0)
counter = 0
cycle = 0


time_quantum = 2


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

def get_input():
    global R

    r1, r2, r3 = map(int, input().split())
    R = [r1, r2, r3]
    

    num_tasks = int(input())

    for i in range(num_tasks):
        task_name, task_type, duration = input().split()
        tasks.append(Task(task_name, task_type, int(duration)))

def schedulable(cpu_index):
    global CPUs, ready_queue, waiting_queue, R

    done = False

    curr_task = CPUs[cpu_index]
    if curr_task.type == "X":
        R[0] += 1
        R[1] += 1
    elif curr_task.type == "Y":
        R[1] += 1
        R[2] += 1
    elif curr_task.type == "Z":
        R[0] += 1
        R[2] += 1

    if waiting_queue != []:
        curr_waiting = waiting_queue[0]
        if curr_waiting.type == "X" and R[0] >= 1 and R[1] >= 1:
            curr_waiting.state = "ready"
            ready_queue.insert(0, waiting_queue.pop(0))
        elif curr_waiting.type == "Y" and R[1] >= 1 and R[2] >= 1:
            curr_waiting.state = "ready"
            ready_queue.insert(0, waiting_queue.pop(0))
        elif curr_waiting.type == "Z" and R[0] >= 1 and R[2] >= 1:
            curr_waiting.state = "ready"
            ready_queue.insert(0, waiting_queue.pop(0))

    for curr_ready in ready_queue:
        if curr_ready.type == "X" and R[0] >= 1 and R[1] >= 1:
            R[0] -= 1
            R[1] -= 1

            curr_ready.state = "running"

            
            CPUs[cpu_index] = ready_queue.pop(0)
            done = True
            break
        elif curr_ready.type == "Y" and R[1] >= 1 and R[2] >= 1:
            R[1] -= 1
            R[2] -= 1

            curr_ready.state = "running"

            CPUs[cpu_index] = ready_queue.pop(0)
            done = True
            break
        elif curr_ready.type == "Z" and R[0] >= 1 and R[2] >= 1:
            R[0] -= 1
            R[2] -= 1

            curr_ready.state = "running"

            CPUs[cpu_index] = ready_queue.pop(0)
            done = True
            break
        else:
            curr_ready.state = "waiting"
            waiting_queue.append(ready_queue.pop(0))

    if done:
        curr_task.time_running += 1

        if curr_task.time_running == curr_task.duration:
            pass
        else:
            ready_queue.append(curr_task)
    else:
        if curr_task.type == "X":
            R[0] -= 1
            R[1] -= 1
        elif curr_task.type == "Y":
            R[1] -= 1
            R[2] -= 1
        elif curr_task.type == "Z":
            R[0] -= 1
            R[2] -= 1

    return done

def execute(cpu_index):
    global ready_queue, counter, cycle, R

    while True:
        semaphore.acquire()
        counter += 1
                

        if CPUs[cpu_index] != "Idle":

            if (cycle % time_quantum == 0):
                if schedulable(cpu_index):
                    if counter == 4:
                        counter = 0
                        semaphore_out.release()
                        cycle += 1

                    semaphore.release()
                    time.sleep(1)
                    continue

            CPUs[cpu_index].time_running += 1

            if CPUs[cpu_index].time_running == CPUs[cpu_index].duration:
                if CPUs[cpu_index].type == "X":
                    R[0] += 1
                    R[1] += 1
                elif CPUs[cpu_index].type == "Y":
                    R[1] += 1
                    R[2] += 1
                elif CPUs[cpu_index].type == "Z":
                    R[0] += 1
                    R[2] += 1

                CPUs[cpu_index] = "Idle"
            else:
                if counter == 4:
                    counter = 0
                    semaphore_out.release()
                    cycle += 1

                semaphore.release()
                time.sleep(1)
                continue

        
        if ready_queue == [] and waiting_queue == []:
            if counter == 4:
                counter = 0
                semaphore_out.release()
                cycle += 1

            semaphore.release()
            time.sleep(1)
            
            continue


        if waiting_queue != []:
            curr_waiting = waiting_queue[0]
            if curr_waiting.type == "X" and R[0] >= 1 and R[1] >= 1:
                curr_waiting.state = "ready"
                ready_queue.insert(0, waiting_queue.pop(0))
            elif curr_waiting.type == "Y" and R[1] >= 1 and R[2] >= 1:
                curr_waiting.state = "ready"
                ready_queue.insert(0, waiting_queue.pop(0))
            elif curr_waiting.type == "Z" and R[0] >= 1 and R[2] >= 1:
                curr_waiting.state = "ready"
                ready_queue.insert(0, waiting_queue.pop(0))

        for curr_task in ready_queue:
            if curr_task.type == "X" and R[0] >= 1 and R[1] >= 1:
                R[0] -= 1
                R[1] -= 1

                curr_task.state = "running"

                CPUs[cpu_index] = ready_queue.pop(0)
                break
            elif curr_task.type == "Y" and R[1] >= 1 and R[2] >= 1:
                R[1] -= 1
                R[2] -= 1

                curr_task.state = "running"

                CPUs[cpu_index] = ready_queue.pop(0)
                break
            elif curr_task.type == "Z" and R[0] >= 1 and R[2] >= 1:
                R[0] -= 1
                R[2] -= 1

                curr_task.state = "running"

                CPUs[cpu_index] = ready_queue.pop(0)
                break
            else:
                curr_task.state = "waiting"
                waiting_queue.append(ready_queue.pop(0))

        if counter == 4:
            counter = 0
            semaphore_out.release()
            cycle += 1

        semaphore.release()
        time.sleep(1)

        

def output():
    cycle_out = 0
    while True:
        semaphore_out.acquire()
        cycle_out += 1
        print(f"time  {cycle_out}")
        for i in range(len(CPUs)):
            print(f"CPU[{i+1}]: {CPUs[i].name if CPUs[i] != 'Idle' else 'Idle'}")
        print("R1:", R[0], "    ", "R2:", R[1], "    ", "R3:", R[2])
        print("ready queue:", [t.name for t in ready_queue])
        print("waiting queue:", [t.name for t in waiting_queue])
        print()

def main():
    global ready_queue

    get_input()

    # sort based on X, Y, Z
    # ready_queue = sorted(tasks, key=lambda x: priority_mapping[x.type])

    # ready_queue = sorted(tasks, key=lambda x: x.duration)
    ready_queue = tasks

    

    threads = []
    for i in range(len(CPUs)):
        thread = threading.Thread(target=execute, args=(i,))
        threads.append(thread)
        thread.start()

    connect_thread = threading.Thread(target=output)
    connect_thread.start()


    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()