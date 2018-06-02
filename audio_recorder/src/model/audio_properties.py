'''
Created on Jun 1, 2018

@author: Nebojsa
'''
import pyaudio

class Audio_properties(object):
    """
    """

    def __init__(self, chunk=1024, audio_format=pyaudio.paInt16, channels=1, rate=16000, record_seconds=15, audio_input=True):
        """
        """
        self.chunk = chunk
        self.audio_format = audio_format
        self.channels = channels
        self.rate = rate
        self.record_seconds = record_seconds
        self.audio_input = audio_input
        
    def get_chunk(self):
        return self.chunk
    
    def get_audio_format(self):
        return self.audio_format
    
    def get_channels(self):
        return self.channels
    
    def get_rate(self):
        return self.rate
    
    def get_record_seconds(self):
        return self.record_seconds
    
    def get_audio_input(self):
        return self.audio_input