import multiprocessing as mp
import os
import random
import time
from datetime import datetime

# Producer function
def producer(producer_id, pipe_name, semaphore):
    with open(pipe_name, 'wb') as pipe:
        while True:
            semaphore.acquire()  # Control overproduction
            items = [random.randint(1, 100) for _ in range(3)]
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Producer {producer_id} produced items: {items}")
            pipe.write(bytes(f"{producer_id}:{items}\n", 'utf-8'))
            pipe.flush()
            semaphore.release()
            time.sleep(random.uniform(1, 3))  # Simulate work

# Consumer function
def consumer(consumer_id, pipe_name, semaphore):
    while True:
        with open(pipe_name, 'rb') as pipe:
            while True:
                line = pipe.readline().decode('utf-8').strip()
                if not line:  # If no data is available, reopen the pipe
                    time.sleep(0.5)  # Wait before retrying
                    break
                producer_id, items = line.split(':')
                items = eval(items)  # Convert string representation to list
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] Consumer {consumer_id} consumed items from Producer {producer_id}: {items}")
                time.sleep(random.uniform(0.5, 1.5))  # Simulate work

if __name__ == "__main__":
    pipe_name = "/tmp/producer_consumer_pipe"

    # Ensure the named pipe exists
    try:
        os.mkfifo(pipe_name)
    except FileExistsError:
        pass

    # Semaphore to control production and consumption limits
    producer_semaphore = mp.Semaphore(3)  # Producer limit
    consumer_semaphore = mp.Semaphore(5)  # Consumer limit

    # Start producers
    producers = [mp.Process(target=producer, args=(i, pipe_name, producer_semaphore)) for i in range(3)]
    for p in producers:
        p.start()

    # Start consumers
    consumers = [mp.Process(target=consumer, args=(i, pipe_name, consumer_semaphore)) for i in range(2)]
    for c in consumers:
        c.start()

    # Join processes
    for p in producers:
        p.join()
    for c in consumers:
        c.join()
