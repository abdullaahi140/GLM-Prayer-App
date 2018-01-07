import psutil


running = []
for proc in psutil.process_iter():
    try:
        if "temp.py" in proc.cmdline()[1]:
            running.append([proc.name(), proc.pid, proc.cmdline()[1]])
    except (psutil._exceptions.AccessDenied, IndexError):
        pass

print(running)
