import time

EC_PATH = "/sys/kernel/debug/ec/ec0/io"
MAX_RPM = 5000  # adjust if needed

def read_ec():
    with open(EC_PATH, "rb") as f:
        return list(f.read())

while True:
    data = read_ec()

    b86 = data[86]
    b88 = data[88]

    fan_level = (b86 + b88) / 2
    rpm = (fan_level / 100) * MAX_RPM

    print(f"Fan level: {fan_level:.1f}% | Estimated RPM: {rpm:.0f}")

    time.sleep(1)


