from flask import Flask, render_template, jsonify
import fastdotcom

app = Flask(__name__)

def run_speed_test():
    download_speed = fastdotcom.fast_com()
    return {"download": f"{download_speed:.2f} Mbps", "upload": "N/A", "ping": "N/A"}


@app.route('/start_speed_test')
def start_speed_test():
    result = run_speed_test()  
    return jsonify(result)  

@app.route('/')
def index():
    return render_template('speedtest.html')

if __name__ == '__main__':
    app.run(port = 5004)
