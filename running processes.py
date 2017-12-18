import psutil
import time

PROCNAME = "pythonw.exe"

for proc in psutil.process_iter():
    if proc.name() == PROCNAME:
        print(proc)

time.sleep(60)
