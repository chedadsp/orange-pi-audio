"""
Created on Jun 1, 2018

@author: Nebojsa
"""
from flask import Flask, Response
from model.audioproperties import AudioProperties
from recorder.recorder import Recorder
from udp_sender.udp_sender import UDPSender

if __name__ == '__main__':
    app = Flask(__name__)

    recorder = Recorder()
    audio_properties = AudioProperties()

    udp_sender = UDPSender()
    udp_sender.start()

    port = 63000
    
    @app.route('/record')
    def record_and_save():
        global recorder
        if recorder.is_recording():
            return "Already recording"
        else:
            recorder = Recorder(audio_properties)
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
    
    @app.route('/set_audio_properties/<int:chunk>/<int:channels>/<int:rate>/<int:audio_input>')
    def set_audio_properties(chunk, channels, rate, audio_input):
        global audio_properties
        audio_properties = AudioProperties(chunk=chunk, channels=channels, rate=rate, audio_input=audio_input)
        return "NEW AUDIO PROPERTIES SET"

    @app.route('/get_recorded_audio')
    def get_recorded_audio():
        try:
            return Response(recorder.get_recorded_audio())
        except Exception as e:
            return str(e)

    # Starting server
    app.run(host='0.0.0.0', port=port)

    udp_sender.stopping_server_message()
    udp_sender.join()

