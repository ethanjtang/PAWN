# Used to print out messages every X seconds during program runtime
# (to check that it is continuing to run over several hours/days)

# imports
import time
import threading

# Timer to print program's elapsed time
def program_timer(sleep_time_in_secs=60):
    start_time = time.time()
    while True:
        time.sleep(sleep_time_in_secs)
        elapsed = int(time.time() - start_time)
        print(f"Program has been running for ~{elapsed} seconds")

# Function to start program timer thread
def start_timer(thread_update_time_secs):
    timer_thread = threading.Thread(target=program_timer, args=(thread_update_time_secs,), daemon=True)
    # daemon=True -> kill thread after program finishes executing without waiting
    timer_thread.start()