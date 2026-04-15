import time

EC_PATH = "/sys/kernel/debug/ec/ec0/io"
CSV_FILE = "focused_ec_log.csv"

WATCH_BYTES = list(range(75, 96)) + list(range(100, 111)) + [86, 88]

def read_ec():
    with open(EC_PATH, "rb") as f:
        return list(f.read())

# header
with open(CSV_FILE, "w") as f:
    header = ["time"] + [f"b{i}" for i in WATCH_BYTES]
    f.write(",".join(header) + "\n")

while True:
    data = read_ec()
    ts = time.strftime("%H:%M:%S")

    row = [ts] + [data[i] for i in WATCH_BYTES]

    print(f"{ts} | FAN: {data[86]}, {data[88]} | CTRL: {data[80]} | TEMP?: {data[100]}")

    with open(CSV_FILE, "a") as f:
        f.write(",".join(map(str, row)) + "\n")

    time.sleep(0.5)
