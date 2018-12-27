'''
Created on Jun 1, 2018

@author: Nebojsa
'''
from flask import Flask, render_template
import requests
import os
import time
from udp_receiver.udp_receiver import UDPReceiver

if __name__ == '__main__':
    app = Flask(__name__)

    port = 62000

    udp_receiver = UDPReceiver()
    udp_receiver.start()

    def check_for_response(response, microphone):
        try:
            response.raise_for_status()
        except Exception as e:
            print("Microphone {} returned status {}".format(microphone, response.status_code))
            print(e)
            udp_receiver.remove_microphone(microphone)

    @app.route('/')
    def index_page():
        return render_template('index.html', text_value='Welcome to recorder.', link='record', button_text='Record',
                               files_button_visible='none')

    @app.route('/record')
    def start_record():
        for microphone in udp_receiver.get_microphones():
            response = requests.get('http://{}:63000/record'.format(microphone))
            check_for_response(response, microphone)

        return render_template('index.html', text_value='Recording...', link='stop_record',
                               button_text='Stop recording', files_button_visible='none')

    @app.route('/stop_record')
    def stop_record():
        for microphone in udp_receiver.get_microphones():
            response = requests.get('http://{}:63000/stop_recording'.format(microphone))
            check_for_response(response, microphone)

        return render_template('index.html', text_value='Start recording again.', link='record', button_text='Record',
                               files_button_visible='visible')

    @app.route('/get_files')
    def get_files():
        if udp_receiver.get_microphones():
            dir_name = time.strftime("%Y-%m-%d-%H-%M-%S")
            new_dir_path = "../output/" + dir_name
            try:
                os.mkdir(new_dir_path)
            except OSError as e:
                print(e)
                return render_template('index.html', text_value='Cannot create output folder {}.'.format(dir_name),
                                       link='record', button_text='Record', files_button_visible='none')

            for index, microphone in enumerate(udp_receiver.get_microphones()):
                response = requests.get('http://{}:63000/get_output_file'.format(microphone))
                check_for_response(response, microphone)
                file_with_path = new_dir_path + "/output" + str(index) + ".wav"
                with open(file_with_path, 'wb') as handle:
                    for block in response.iter_content(1024):
                        handle.write(block)

            return render_template('index.html', text_value='Files have been downloaded and saved in {}.'
                                   .format(dir_name), link='record', button_text='Record', files_button_visible='none')
        else:
            return render_template('index.html', text_value='No connected microphones.', link='record',
                                   button_text='Record', files_button_visible='none')

    # Starting server
    app.run(host='0.0.0.0', port=port)

    udp_receiver.shutdown()
    udp_receiver.join()


