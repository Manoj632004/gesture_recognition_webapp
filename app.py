from flask import Flask, render_template, Response
from new import VideoCapture
import os
import signal

app = Flask(__name__)
video_capture = VideoCapture()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main_video_feed')
def main_video_feed():
    return Response(VideoCapture.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

"""
@app.route('/toggle_video', methods=['POST'])
def toggle_video():
    video_capture.toggle_video()
    return 'Video toggled successfully.', 200
"""
if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True)
    

