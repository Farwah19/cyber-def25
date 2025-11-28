import os
import random
from datetime import datetime, timedelta

OUTPUT_DIR = "network_logs"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def random_timestamp():
    now = datetime.now()
    delta = timedelta(seconds=random.randint(0, 86400))
    return (now - delta).strftime("%Y-%m-%d %H:%M:%S")

def generate_log_entry():
    return (
        f"{random_timestamp()}  "
        f"SRC={random_ip()}  "
        f"DST={random_ip()}  "
        f"SPORT={random.randint(1, 65535)}  "
        f"DPORT={random.randint(1, 65535)}  "
        f"BYTES_SENT={random.randint(0, 30000)}  "
        f"BYTES_RECV={random.randint(0, 30000)}  "
        f"ENTROPY={round(random.uniform(1.0, 7.0), 2)}  "
        f"FLAGS={random.randint(0, 63)}  "
        f"FAILED_LOGINS={random.randint(0, 4)}  "
        f"MALFORMED={random.randint(0, 2)}"
    )

def generate_log_file(index):
    num_entries = random.randint(50, 200)
    filename = os.path.join(OUTPUT_DIR, f"logfile_{index}.log")

    with open(filename, "w") as f:
        for _ in range(num_entries):
            f.write(generate_log_entry() + "\n")

    print(f"Generated {filename} with {num_entries} entries.")

# Generate 10 logs
for i in range(1, 11):
    generate_log_file(i)

print("All test log files generated successfully!")
