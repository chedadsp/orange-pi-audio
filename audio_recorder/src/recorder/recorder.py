'''
Created on Jun 1, 2018

@author: Nebojsa
'''
import pyaudio
import wave
from model.audio_properties import Audio_properties

class Recorder(object):
    '''
    classdocs
    '''

    def __init__(self, audio_properties=Audio_properties(), output_file_path="../output/test.wav"):
        '''
        Constructor
        '''
        self.audio_properties = audio_properties
        self.output_file_path = output_file_path
        
    def set_audio_properties(self, audio_properties):
        self.audio_properties = audio_properties
        
    def set_output_file_path(self, output_file_path):
        self.output_file_path = output_file_path
        
    def record_and_save(self):

        p = pyaudio.PyAudio()

        audio_format=self.audio_properties.get_audio_format()
        channels=self.audio_properties.get_channels()
        rate=self.audio_properties.get_rate()
        audio_input=self.audio_properties.get_audio_input()
        frames_per_buffer=self.audio_properties.get_chunk()
        record_seconds=self.audio_properties.get_record_seconds()
        
        stream = p.open(format=audio_format,
                        channels=channels,
                        rate=rate,
                        input=audio_input,
                        frames_per_buffer=frames_per_buffer)

        print("* recording")

        frames = []

        for i in range(0, int(rate / frames_per_buffer * record_seconds)):
            data = stream.read(frames_per_buffer)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.output_file_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()