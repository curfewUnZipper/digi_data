import time
import multiprocessing as mp
import math
import psutil
import os
import signal
import subprocess

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


# ===== NVIDIA GPU =====
def read_nvidia():
    try:
        output = subprocess.check_output([
            "nvidia-smi",
            "--query-gpu=utilization.gpu,power.draw,temperature.gpu",
            "--format=csv,noheader,nounits"
        ]).decode().strip()

        util, power, temp = map(float, output.split(", "))
        return util, power, temp
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
    print("🔥 Ultimate Logger (FULL HYBRID MODE)")
    print("Cycle: NO → LOW → MED → HIGH\n")

    num_cores = psutil.cpu_count()

    # ===== CSV HEADER =====
    core_headers = ",".join([f"cpu_core_{i}" for i in range(num_cores)])

    with open(LOG_FILE, "w") as f:
        f.write(
            "timestamp,time,load,"
            "cpu_usage,gpu_power,"
            f"{core_headers},"
            "cpu_freq,"
            "cpu_temp,gpu_temp,"
            "current,voltage,power,"
            "proc_count,"
            "nvidia_util,nvidia_power,nvidia_temp,"
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

                # ===== CPU =====
                cpu = psutil.cpu_percent()
                cpu_cores = psutil.cpu_percent(percpu=True)
                freq = psutil.cpu_freq()
                cpu_freq = freq.current if freq else 0

                # ===== GPU (AMD iGPU) =====
                gpu_p = safe_read(GPU_POWER_PATH, 1_000_000)

                # ===== GPU (NVIDIA dGPU) =====
                n_util, n_power, n_temp = read_nvidia()

                # ===== TEMPS =====
                cpu_t = safe_read(CPU_TEMP_PATH, 1000)
                gpu_t = safe_read(GPU_TEMP_PATH, 1000)

                # ===== POWER =====
                curr, volt, power = read_battery()

                # ===== SYSTEM =====
                proc_count = len(psutil.pids())

                # ===== EC =====
                fan1, fan2, stage = read_ec()

                core_values = ",".join([f"{c:.1f}" for c in cpu_cores])

                line = (
                    f"{t},{timestr},{load},"
                    f"{cpu:.1f},{gpu_p:.2f},"
                    f"{core_values},"
                    f"{cpu_freq:.1f},"
                    f"{cpu_t:.1f},{gpu_t:.1f},"
                    f"{curr:.3f},{volt:.2f},{power:.2f},"
                    f"{proc_count},"
                    f"{n_util:.1f},{n_power:.1f},{n_temp:.1f},"
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
