import threading

def thread_function(thread_id):
    print(f"Thread {thread_id} is running")

if __name__ == "__main__":
    threads = []
    for i in range(4):
        thread = threading.Thread(target=thread_function, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
