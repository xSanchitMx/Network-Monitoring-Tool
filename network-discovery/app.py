from flask import Flask, render_template, jsonify
import subprocess
import re

app = Flask(__name__)

def scan_network():
    devices = []
    try:
        output = subprocess.check_output("arp -a", shell=True, text=True)
        matches = re.findall(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9A-Fa-f:-]{17})", output)

        for ip, mac in matches:
            devices.append({"ip": ip, "mac": mac})

    except Exception as e:
        return [{"error": f"Failed to scan network: {str(e)}"}]

    return devices

@app.route('/')
def index():
    return render_template('network_discovery.html')

@app.route('/scan')
def scan():
    devices = scan_network()
    return jsonify(devices)

if __name__ == '__main__':
    app.run(port=5005, debug=True)
