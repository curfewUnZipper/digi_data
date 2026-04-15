import time
import multiprocessing
import math

# ===== CONFIG =====
EC_PATH = "/sys/kernel/debug/ec/ec0/io"
BAT_PATH = "/sys/class/power_supply/BAT1"

LOAD_SEQUENCE = ["NO_LOAD", "LOW", "MED", "HIGH"]
LOAD_CORES = {
    "NO_LOAD": 0,
    "LOW": 2,
    "MED": 4,
    "HIGH": 8
}

INTERVAL = 30  # seconds per load level

workers = []

# ===== CPU LOAD =====
def stress():
    x = 0
    while True:
        x += math.sqrt(12345)

def set_load(label):
    global workers

    # stop existing workers
    for p in workers:
        p.terminate()
    workers.clear()

    cores = LOAD_CORES[label]

    for _ in range(cores):
        p = multiprocessing.Process(target=stress)
        p.start()
        workers.append(p)

# ===== READ EC =====
def read_ec():
    with open(EC_PATH, "rb") as f:
        return list(f.read())

# ===== READ BATTERY =====
def read_battery():
    with open(f"{BAT_PATH}/current_now") as f:
        curr = int(f.read().strip())
    with open(f"{BAT_PATH}/voltage_now") as f:
        volt = int(f.read().strip())

    curr_A = curr / 1_000_000
    volt_V = volt / 1_000_000
    power_W = curr_A * volt_V

    return curr_A, volt_V, power_W

# ===== MAIN =====
def main():
    print("🔥 Starting cyclic logger...")
    print("Cycle: NO_LOAD → LOW → MED → HIGH (every 30s)\n")

    with open("full_log.csv", "w") as f:
        f.write("time,load,current_A,voltage_V,power_W,fan1,fan2,stage\n")

    try:
        while True:
            for load_label in LOAD_SEQUENCE:
                print(f"\n⚙️ Switching to: {load_label}")
                set_load(load_label)

                start_time = time.time()

                while time.time() - start_time < INTERVAL:
                    ts = time.strftime("%H:%M:%S")

                    curr_A, volt_V, power_W = read_battery()
                    data = read_ec()

                    fan1 = data[86]
                    fan2 = data[88]
                    stage = data[85]

                    line = f"{ts},{load_label},{curr_A:.3f},{volt_V:.2f},{power_W:.2f},{fan1},{fan2},{stage}"

                    print(line)

                    with open("full_log.csv", "a") as f:
                        f.write(line + "\n")

                    time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
        for p in workers:
            p.terminate()

if __name__ == "__main__":
    main()
