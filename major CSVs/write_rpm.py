import time

EC_PATH = "/sys/kernel/debug/ec/ec0/io"
MAX_RPM = 5000

# ===== SET YOUR TARGET RPM HERE =====
target_rpm = 4000   # <-- change this value

# Convert to fan %
target_level = (target_rpm / MAX_RPM) * 100

print(f"Target RPM: {target_rpm}")
print(f"Target level: {target_level:.1f}%")

def read_ec():
    with open(EC_PATH, "rb") as f:
        return list(f.read())

def write_ec(index, value):
    with open(EC_PATH, "r+b") as f:
        f.seek(index)
        f.write(bytes([value]))

while True:
    data = read_ec()

    b86 = data[86]
    b88 = data[88]

    current_level = (b86 + b88) / 2

    print(f"Current level: {current_level:.1f}% | Target: {target_level:.1f}%")

    # ===== CONTROL LOGIC =====
    if current_level < target_level - 2:
        new_val = min(b86 + 1, 100)
        write_ec(86, new_val)

    elif current_level > target_level + 2:
        new_val = max(b86 - 1, 0)
        write_ec(86, new_val)

    time.sleep(0.5)
