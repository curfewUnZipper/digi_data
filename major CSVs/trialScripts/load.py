import multiprocessing
import time
import math

def stress_cpu():
    x = 0
    while True:
        x += math.sqrt(12345)  # keep CPU busy

def run_load(seconds=30, cores=4):
    procs = []

    print(f"🔥 Applying load for {seconds}s on {cores} cores...")

    for _ in range(cores):
        p = multiprocessing.Process(target=stress_cpu)
        p.start()
        procs.append(p)

    time.sleep(seconds)

    print("🛑 Stopping load...")

    for p in procs:
        p.terminate()

if __name__ == "__main__":
    run_load(seconds=60, cores=6)
