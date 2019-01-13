'''
Created on Jun 1, 2018

@author: Nebojsa
'''
from flask import Flask, send_file
from model.audio_properties import Audio_properties
from recorder.recorder import Recorder
from udp_sender.udp_sender import UDPSender
import os

if __name__ == '__main__':
    app = Flask(__name__)

    recorder = Recorder()
    audio_properties = Audio_properties()
    output_file_path = "../output/test.wav"

    udp_sender = UDPSender()
    udp_sender.send_message()

    port = 63000
    
    @app.route('/record')
    def record_and_save():
        global recorder
        if recorder.is_recording():
            return "Already recording"
        else:
            recorder = Recorder(audio_properties, output_file_path)
            recorder.start()
            return "Recording"

    @app.route('/stop_recording')
    def stop_recording():
        if not recorder.is_recording():
            return "Not recording"
        else:
            recorder.stop_recording()
            recorder.join()
            return "Stopped recording"
    
    @app.route('/set_audio_properties/<int:chunk>/<int:channels>/<int:rate>/<int:record_seconds>/<int:audio_input>')
    def set_audio_properties(chunk, channels, rate, record_seconds, audio_input):
        global audio_properties
        audio_properties = Audio_properties(chunk=chunk, channels=channels, rate=rate, record_seconds=record_seconds, audio_input=audio_input)
        return "NEW AUDIO PROPERTIES SET"
    
    @app.route('/set_output_path/<path:path>')
    def set_output_path(path):
        global output_file_path
        output_file_path = path
        return "NEW FILE PATH SET"

    @app.route('/get_output_file')
    def get_output_file():
        try:
            full_path = os.path.join(os.path.abspath(__file__), "..", output_file_path)
            file_name = full_path.split('/')[-1]
            return send_file(output_file_path, attachment_filename=file_name)
        except Exception as e:
            return str(e)

    # Starting server
    app.run(host='0.0.0.0', port=port)

    udp_sender.send_message()


