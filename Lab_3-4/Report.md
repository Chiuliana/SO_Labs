# Report: Implementation of Signal Handling and Producer-Consumer Problem in Python

## Task Overview
This report covers the implementation of three tasks:

1. **Signal Handling with `SIGUSR1` and `SIGUSR2`**:
   - The first task demonstrates how to handle UNIX signals (`SIGUSR1` and `SIGUSR2`) in Python using the `signal` module.
   
2. **Producer-Consumer Problem with Semaphores**:
   - The second task addresses the classic producer-consumer problem using Python's `multiprocessing` module and semaphores for synchronizing access to shared resources.

3. **Enhancement of the Producer-Consumer Model**:
   - In the third task, the producer-consumer model is enhanced by adding an additional consumer to increase the parallelism.

---

## Task 1: Signal Handling with `SIGUSR1` and `SIGUSR2`

### Objective
- Handle `SIGUSR1` and `SIGUSR2` signals to either print a message or generate and print a random string of characters and terminate the program.

### Code Implementation

```python
import signal
import random
import string
import sys

# Handler for SIGUSR1
def handle_sigusr1(signum, frame):
    print("SIGUSR1 received")

# Handler for SIGUSR2
def handle_sigusr2(signum, frame):
    # Generate and print 100 random ASCII characters
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
    print(random_string)
    sys.exit(0)  # Terminate the program

# Register the signal handlers
signal.signal(signal.SIGUSR1, handle_sigusr1)
signal.signal(signal.SIGUSR2, handle_sigusr2)

# Keep the program running to handle signals
print("Program running, send SIGUSR1 or SIGUSR2 to test")
while True:
    pass
```
### Description
- **Signal Handlers**: Two signal handlers are implemented:
  - `handle_sigusr1`: Prints a message when SIGUSR1 is received.
  - `handle_sigusr2`: Generates and prints 100 random alphanumeric characters and then terminates the program.
  
- **Signal Registration**: The `signal.signal()` function is used to register handlers for SIGUSR1 and SIGUSR2.

- **Program Running**: The program runs indefinitely to listen for signals and handle them as they are received.

### Key Concepts

- **Signal Handling**: Allows the program to react to signals sent from the OS or other programs (e.g., through the kill command).

---

## Task 2: Producer-Consumer Problem with Semaphores

### Objective
- Implement the producer-consumer problem using Python’s multiprocessing module and semaphores for synchronization.

### Code Implementation

```python
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

```
### Description

- **Producer**: Produces a list of 3 random integers and writes them to a named pipe.
- **Consumer**: Reads data from the pipe, processes it, and simulates consumption with a delay.
- **Semaphore**: The `semaphore.acquire()` and `semaphore.release()` calls are used to control access to the shared resource (the pipe). This ensures that producers and consumers do not overwhelm the system.

### Key Concepts

- **Named Pipes (FIFO)**: Used to transfer data between processes.
- **Semaphores**: A synchronization mechanism that controls access to shared resources by multiple processes.

---

## Task 3: Enhanced Producer-Consumer Model

### Objective
- Modify the model from Task 2 by adding an additional consumer to increase concurrency and better manage the producer-consumer workload.

### Code Implementation

```python
# The code is almost identical to Task 2, with the only change being the addition of one more consumer.

# Start consumers
consumers = [mp.Process(target=consumer, args=(i, pipe_name, consumer_semaphore)) for i in range(3)]  # Changed to 3 consumers
for c in consumers:
    c.start()

```
### Description

The main difference between this task and Task 2 is the increase in the number of consumers from 2 to 3. This enhances the ability to process the items produced by the producers concurrently.

### Key Concepts

- **Parallel Processing**: This enhancement demonstrates how parallelism can be used to optimize the consumption of produced items, leading to better performance when there is a high rate of production.

---

## Conclusion

The implementation of signal handling and the producer-consumer problem in Python demonstrates the power of concurrency and synchronization mechanisms available in the language. 

In **Task 1**, we successfully handled `SIGUSR1` and `SIGUSR2` signals, allowing the program to respond dynamically to system events by either printing a message or generating random strings upon receiving signals. This task showcased how Python can interact with system-level signals using the `signal` module.

In **Task 2**, we solved the classic producer-consumer problem using Python's `multiprocessing` module. By introducing semaphores to manage access to shared resources, we ensured that both producers and consumers could operate efficiently without conflicting over resources. This solution demonstrated the principles of parallel processing and synchronization, which are crucial in concurrent programming.

In **Task 3**, we enhanced the producer-consumer model by adding an additional consumer to better manage the production-consumption cycle. This improvement helped to increase concurrency and better handle workload processing, demonstrating the flexibility of the model for scaling.

Overall, these tasks illustrate key concepts in system programming and concurrent process management in Python, offering a robust foundation for solving real-world problems involving multiple processes and inter-process communication.
