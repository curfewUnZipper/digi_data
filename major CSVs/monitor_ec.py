import time

EC_PATH = "/sys/kernel/debug/ec/ec0/io"
CSV_FILE = "ec_segment_log.csv"

def read_ec():
    with open(EC_PATH, "rb") as f:
        return list(f.read())

# ===== Write CSV header =====
with open(CSV_FILE, "w") as f:
    header = ["time", "fan86", "fan88"] + [f"b{i}" for i in range(60, 120)]
    f.write(",".join(header) + "\n")

while True:
    data = read_ec()

    ts = time.strftime("%H:%M:%S")

    fan1 = data[86]
    fan2 = data[88]

    segment = data[60:120]

    # ===== Print live =====
    print(f"{ts} | FAN: {fan1}, {fan2}")

    # ===== Write CSV =====
    row = [ts, fan1, fan2] + segment

    with open(CSV_FILE, "a") as f:
        f.write(",".join(map(str, row)) + "\n")

    time.sleep(0.5)






