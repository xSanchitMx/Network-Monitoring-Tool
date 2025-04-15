from flask import Flask, jsonify, render_template
import psutil
import time

app = Flask(__name__)

prev_stats = psutil.net_io_counters()
prev_time = time.time()

def convert_bytes(bytes):
    if bytes < 1024:
        return round(bytes / 1024, 2), "KB"
    elif bytes < 1024**2:
        return round(bytes / 1024, 2), "KB" 
    elif bytes < 1024**3:
        return round(bytes / 1024**2, 2), "MB"  
    elif bytes < 1024**4:
        return round(bytes / 1024**3, 2), "GB"  
    else:
        return round(bytes / 1024**4, 2), "TB"

@app.route('/')
def index():
    return render_template('network_stats.html')

@app.route('/stats')
def get_network_stats():
    global prev_stats, prev_time
    
    current_stats = psutil.net_io_counters()
    current_time = time.time()

    interval = current_time - prev_time
    download_speed = (current_stats.bytes_recv - prev_stats.bytes_recv) / interval
    upload_speed = (current_stats.bytes_sent - prev_stats.bytes_sent) / interval

    received, received_unit = convert_bytes(current_stats.bytes_recv)
    sent, sent_unit = convert_bytes(current_stats.bytes_sent)
    receiving = round(download_speed / 1024, 2)  # in KB/s
    sending = round(upload_speed / 1024, 2)  # in KB/s

    prev_stats = current_stats
    prev_time = current_time

    return jsonify({
        "received": f"{received} {received_unit}",
        "sent": f"{sent} {sent_unit}",
        "receiving": f"{receiving} KB/s",
        "sending": f"{sending} KB/s"
    })

if __name__ == '__main__':
    app.run(port=5001)
