from flask import Flask, render_template, jsonify
import subprocess
import platform
import re
import statistics
import time

app = Flask(__name__)

def ping_host(host="8.8.8.8", count=5):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        output = subprocess.run(["ping", param, str(count), host], capture_output=True, text=True, check=True)
        return output.stdout
    except subprocess.CalledProcessError:
        return "Ping failed"

def extract_ping_times(output):
    times = []
    if platform.system().lower() == "windows":
        matches = re.findall(r"time=([0-9]+)ms", output)
    else:
        matches = re.findall(r"time=([0-9]+\.?[0-9]*) ms", output)
    
    for match in matches:
        times.append(float(match))
    return times

def measure_jitter(host="8.8.8.8", count=5):
    ping_output = ping_host(host, count)
    times = extract_ping_times(ping_output)
    if len(times) > 1:
        jitter = statistics.stdev(times)
        return f"{jitter:.2f} ms"
    return "0.00 ms"

@app.route('/')
def index():
    return render_template('ping_jitter.html')

@app.route('/ping_jitter')
def ping_jitter():
    ping_result = ping_host()
    jitter_result = measure_jitter()
    return jsonify({"ping_result": ping_result, "jitter": jitter_result})

@app.route('/restart_test')
def restart_test():
    return jsonify({"message": "Test restarted"})

if __name__ == '__main__':
    app.run(port=5002)
