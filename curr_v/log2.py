import time
import multiprocessing as mp
import math
import psutil
import os
import signal

# ===== CONFIG =====
EC_PATH = "/sys/kernel/debug/ec/ec0/io"
BAT_PATH = "/sys/class/power_supply/BAT1"

LOAD_SEQUENCE = ["NO_LOAD", "LOW", "MED", "HIGH"]
LOAD_CORES = {"NO_LOAD": 0, "LOW": 2, "MED": 4, "HIGH": 8}
INTERVAL = 180
TOTAL_RUNTIME = 3600

LOG_FILE = "ultimate_log.csv"

workers = []
running = True


# ===== CPU LOAD =====
def stress():
    x = 0
    while True:
        x += math.sqrt(12345)


def set_load(label):
    global workers

    for p in workers:
        p.terminate()
    workers.clear()

    for _ in range(LOAD_CORES[label]):
        p = mp.Process(target=stress)
        p.start()
        workers.append(p)


# ===== SENSOR HELPERS =====
def safe_read(path, scale=1):
    try:
        with open(path) as f:
            return int(f.read().strip()) / scale
    except:
        return 0


def read_ec():
    try:
        with open(EC_PATH, "rb") as f:
            data = list(f.read())
            return data[86], data[88], data[85]
    except:
        return 0, 0, 0


def read_battery():
    try:
        curr = safe_read(f"{BAT_PATH}/current_now", 1_000_000)
        volt = safe_read(f"{BAT_PATH}/voltage_now", 1_000_000)
        return curr, volt, curr * volt
    except:
        return 0, 0, 0


# ===== AUTO HWMON DETECTION =====
def find_hwmon(keyword, file):
    base = "/sys/class/hwmon"
    for d in os.listdir(base):
        try:
            name = open(f"{base}/{d}/name").read().strip()
            if keyword in name:
                return f"{base}/{d}/{file}"
        except:
            continue
    return None


CPU_TEMP_PATH = find_hwmon("k10temp", "temp1_input")
GPU_TEMP_PATH = find_hwmon("amdgpu", "temp1_input")
GPU_POWER_PATH = find_hwmon("amdgpu", "power1_input")


# ===== CLEAN EXIT =====
def shutdown(sig, frame):
    global running
    running = False
    print("\n🛑 Graceful shutdown...")


signal.signal(signal.SIGINT, shutdown)


# ===== MAIN LOGGER =====
def main():
    print("🔥 Ultimate Logger (Production Mode)")
    print("Cycle: NO → LOW → MED → HIGH\n")

    # header
    with open(LOG_FILE, "w") as f:
        f.write(
            "timestamp,time,load,"
            "cpu_usage,gpu_power,"
            "cpu_temp,gpu_temp,"
            "current,voltage,power,"
            "fan1,fan2,stage\n"
        )

    start_global = time.time()

    while running and (time.time() - start_global < TOTAL_RUNTIME):
        for load in LOAD_SEQUENCE:
            if not running or (time.time() - start_global >= TOTAL_RUNTIME):
                break

            print(f"\n⚙️ Load: {load}")
            set_load(load)

            start = time.time()

            while time.time() - start < INTERVAL and running:
                t = time.time()
                timestr = time.strftime("%H:%M:%S")

                cpu = psutil.cpu_percent()
                gpu_p = safe_read(GPU_POWER_PATH, 1_000_000)

                cpu_t = safe_read(CPU_TEMP_PATH, 1000)
                gpu_t = safe_read(GPU_TEMP_PATH, 1000)

                curr, volt, power = read_battery()
                fan1, fan2, stage = read_ec()

                line = (
                    f"{t},{timestr},{load},"
                    f"{cpu:.1f},{gpu_p:.2f},"
                    f"{cpu_t:.1f},{gpu_t:.1f},"
                    f"{curr:.3f},{volt:.2f},{power:.2f},"
                    f"{fan1},{fan2},{stage}\n"
                )

                print(line.strip())

                with open(LOG_FILE, "a") as f:
                    f.write(line)

                time.sleep(1)

    # cleanup
    for p in workers:
        p.terminate()


if __name__ == "__main__":
    main()
