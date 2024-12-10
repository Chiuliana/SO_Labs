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
