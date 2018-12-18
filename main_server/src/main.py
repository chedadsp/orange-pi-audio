'''
Created on Jun 1, 2018

@author: Nebojsa
'''
from flask import Flask, render_template
import requests
import miniupnpc

if __name__ == '__main__':
    app = Flask(__name__)

    port = 62000

    # Setting upnp
    upnp = miniupnpc.UPnP()
    
    upnp.discoverdelay = 200
    ndevices = upnp.discover()
    print(ndevices, 'device(s) detected')
    try:
        upnp.selectigd()
        # addportmapping(external-port, protocol, internal-host, internal-port, description, remote-host)
        result = upnp.addportmapping(port, 'TCP', upnp.lanaddr, port, 'testing', '')
        
        print (result)
    except Exception as e:
        print("Exception : ", e)

    @app.route('/')
    def index_page():
        return render_template('index.html', text_value = 'Welcome to recorder.', link = 'record', button_text = 'Record')
    
    @app.route('/record')
    def start_record():
        requests.get('http://localhost:63000/record')
        return render_template('index.html', text_value = 'Recording...', link = 'stop_record', button_text = 'Stop recording')

    @app.route('/stop_record')
    def stop_record():
        requests.get('http://localhost:63000/stop_recording')
        return render_template('index.html', text_value = 'Start recording again.', link = 'record', button_text = 'Record')

    # Starting server
    app.run(host='0.0.0.0', port=port) 


