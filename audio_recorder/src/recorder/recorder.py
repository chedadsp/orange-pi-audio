"""
Created on Jun 1, 2018

@author: Nebojsa
"""
import pyaudio
import threading
from model.audioproperties import AudioProperties


class Recorder(threading.Thread):

    def __init__(self, audio_properties=AudioProperties()):
        threading.Thread.__init__(self)
        self.audio_properties = audio_properties
        self.__recorded_audio = []
        self.__is_recording = False

    def run(self):
        print("Start recording thread.")
        self.record_and_save()
        print("End recording thread.")

    def set_audio_properties(self, audio_properties):
        self.audio_properties = audio_properties

    def is_recording(self):
        return self.__is_recording
        
    def record_and_save(self):

        p = pyaudio.PyAudio()

        audio_format = self.audio_properties.get_audio_format()
        channels = self.audio_properties.get_channels()
        rate = self.audio_properties.get_rate()
        audio_input = self.audio_properties.get_audio_input()
        frames_per_buffer = self.audio_properties.get_chunk()
        
        stream = p.open(format=audio_format,
                        channels=channels,
                        rate=rate,
                        input=audio_input,
                        frames_per_buffer=frames_per_buffer)

        print("* recording")
        self.__is_recording = True
        frames = []
        while self.__is_recording:
            data = stream.read(frames_per_buffer)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        self.__recorded_audio = frames

    def stop_recording(self):
        self.__is_recording = False

    def get_recorded_audio(self):
        return self.__recorded_audio
