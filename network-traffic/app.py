from flask import Flask, render_template, jsonify
import psutil

app = Flask(__name__)

def get_network_usage():
    connections = psutil.net_connections(kind='inet')
    process_usage = {}

    for conn in connections:
        if conn.pid is None:
            continue

        try:
            proc = psutil.Process(conn.pid)
            name = proc.name()

            io_counters = proc.io_counters()
            sent = io_counters[0]  
            recv = io_counters[1]  

            if name in process_usage:
                process_usage[name]['sent'] += sent
                process_usage[name]['recv'] += recv
            else:
                process_usage[name] = {'sent': sent, 'recv': recv}
        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue 

    return process_usage

@app.route('/')
def index():
    return render_template('network_usage.html')

@app.route('/network_usage')
def network_usage():
    usage_data = get_network_usage()
    return jsonify(usage_data)

if __name__ == '__main__':
    app.run(port=5003)
