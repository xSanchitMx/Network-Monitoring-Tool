import subprocess

apps = [
    {"folder": "network-traffic", "port": 5001},
    {"folder": "network-usage", "port": 5002},
    {"folder": "ping-jitter-test", "port": 5003},
    {"folder": "speed-test", "port": 5004},
    {"folder": "network-discovery", "port": 5005}
]

processes = []

for app in apps:
    command = f"python {app['folder']}/app.py"
    process = subprocess.Popen(command, shell=True)
    processes.append(process)

