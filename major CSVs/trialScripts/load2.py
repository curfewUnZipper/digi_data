import multiprocessing
import time
import math

EC_PATH = "/sys/kernel/debug/ec/ec0/io"

target_stage = 7   # 🔥 SET YOUR DESIRED FAN LEVEL

workers = []

def stress():
    x = 0
    while True:
        x += math.sqrt(12345)

def read_ec():
    with open(EC_PATH, "rb") as f:
        return list(f.read())

def add_worker():
    p = multiprocessing.Process(target=stress)
    p.start()
    workers.append(p)

def remove_worker():
    if workers:
        p = workers.pop()
        p.terminate()

print(f"🎯 Target Stage: {target_stage}")

try:
    while True:
        data = read_ec()

        stage = data[85]
        fan1 = data[86]
        fan2 = data[88]

        print(f"\rStage: {stage} | Fan: {fan1},{fan2} | Workers: {len(workers)}", end="")

        # ===== CONTROL LOGIC =====
        if stage < target_stage:
            add_worker()  # increase heat

        elif stage > target_stage:
            remove_worker()  # reduce heat

        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping...")
    for p in workers:
        p.terminate()
