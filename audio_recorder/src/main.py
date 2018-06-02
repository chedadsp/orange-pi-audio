'''
Created on Jun 1, 2018

@author: Nebojsa
'''
from flask import Flask 
from model.audio_properties import Audio_properties
from recorder.recorder import Recorder

if __name__ == '__main__':
    app = Flask(__name__)
    recorder = Recorder()
    
    @app.route('/record')
    def record_and_save():
        recorder.record_and_save()
        return "DONE"
    
    @app.route('/set_audio_properties/<int:chunk>/<int:channels>/<int:rate>/<int:record_seconds>/<int:audio_input>')
    def set_audio_propeties(chunk, channels, rate, record_seconds, audio_input):
        "nisam uspeo namestiti audio format jer se poziva python enumeracija da bi se dobila"
        audio_properties = Audio_properties(chunk=chunk, channels=channels, rate=rate, record_seconds=record_seconds, audio_input=audio_input)
        recorder.set_audio_properties(audio_properties)
        return "NEW AUDIO PROPERTIES SET"
    
    @app.route('/set_output_path/<path:path>')
    def set_output_path(path):
        recorder.set_output_file_path(path)
        return "NEW FILE PATH SET"

    app.run(host='0.0.0.0', port=297) 
