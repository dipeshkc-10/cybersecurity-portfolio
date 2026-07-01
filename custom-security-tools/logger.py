import os
from datetime import datetime

# always write logs/ next to this file, no matter where you run main.py from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "logs", "log.txt")

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)


def log(ip, command, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {ip} >>> {command} | {response}\n"
    print(line, end="")
    with open(LOG_PATH, "a") as f:
        f.write(line)