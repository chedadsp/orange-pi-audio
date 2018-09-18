'''
Created on Jun 1, 2018

@author: Nebojsa
'''
from flask import Flask, send_file, request
from model.audio_properties import Audio_properties
from recorder.recorder import Recorder
import os
import socket
import miniupnpc

if __name__ == '__main__':
    app = Flask(__name__)
    recorder = Recorder()

    port = 29700
    
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

    @app.route('/get_output_file')
    def get_output_file():
        try:
            full_path = os.path.join(os.path.abspath(__file__), "..", recorder.get_output_file_path())
            file_name = full_path.split('/')[-1]
            return send_file(full_path, attachment_filename=file_name)
        except Exception as e:
            return str(e)

    hostname = "nrajic-ZBook-15-G4"
    
    # Finding personal IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        print ("IP Address: %s" %ip)
    except Exception as e:
        print (str(e))
        ip = '127.0.0.1'
    finally:
        s.close()
        
    # Setting upnp
    upnp = miniupnpc.UPnP()

    upnp.discoverdelay = 10
    upnp.discover()

    upnp.selectigd()
    
    # addportmapping(external-port, protocol, internal-host, internal-port, description, remote-host)
    result=upnp.addportmapping(port, 'TCP', upnp.lanaddr, port, 'testing', '')
    
    print (result)

    # Starting server
    app.run(host='0.0.0.0', port=port) 


