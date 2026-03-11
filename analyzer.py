import wave
import numpy as np
import os

class WaveAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.metadata = {}
        self.audio_data = None
        self.time_array = None
        
        self._analyze()

    def _analyze(self):
        try:
            with wave.open(self.filepath, 'rb') as wav_file:
                # Extract metadata
                self.metadata['n_channels'] = wav_file.getnchannels()
                self.metadata['sample_width'] = wav_file.getsampwidth()
                self.metadata['framerate'] = wav_file.getframerate()
                self.metadata['n_frames'] = wav_file.getnframes()
                self.metadata['comp_type'] = wav_file.getcomptype()
                self.metadata['comp_name'] = wav_file.getcompname()
                
                # Calculate duration
                duration = self.metadata['n_frames'] / float(self.metadata['framerate'])
                self.metadata['duration'] = duration
                
                # Read audio data
                raw_data = wav_file.readframes(self.metadata['n_frames'])
                
                # Convert to numpy array based on sample width
                if self.metadata['sample_width'] == 1:
                    dtype = np.uint8
                elif self.metadata['sample_width'] == 2:
                    dtype = np.int16
                elif self.metadata['sample_width'] == 4:
                    dtype = np.int32
                else:
                    raise ValueError(f"Unsupported sample width: {self.metadata['sample_width']} bytes")
                
                data = np.frombuffer(raw_data, dtype=dtype)
                
                # Normalize if 8-bit (uint8)
                if self.metadata['sample_width'] == 1:
                    data = data.astype(np.float32) - 128.0
                
                # Reshape for multi-channel
                if self.metadata['n_channels'] > 1:
                    data = data.reshape(-1, self.metadata['n_channels'])
                
                self.audio_data = data
                
                # Create time array
                self.time_array = np.linspace(0, duration, num=self.metadata['n_frames'])
                
        except Exception as e:
            raise Exception(f"Failed to analyze wave file: {str(e)}")

    def get_metadata_string(self):
        m = self.metadata
        return (
            f"File: {self.filename}\n\n"
            f"Channels: {m.get('n_channels')}\n"
            f"Sample Rate: {m.get('framerate')} Hz\n"
            f"Bit Depth: {m.get('sample_width') * 8} bits\n"
            f"Duration: {m.get('duration'):.2f} seconds\n"
            f"Frames: {m.get('n_frames')}"
        )
