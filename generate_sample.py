import numpy as np
import wave

# Parameters
duration = 3.0  # seconds
framerate = 44100  # Hz
freq = 440.0  # Hz (A4)
amplitude = 0.5

# Generate time array
t = np.linspace(0, duration, int(framerate * duration), False)

# Generate a sweep (chirp) sound for a clear spectrogram
freq_start = 100
freq_end = 2000
sound_wave = amplitude * np.sin(2 * np.pi * np.linspace(freq_start, freq_end, len(t)) * t)

# Add some noise
noise = np.random.normal(0, 0.05, len(t))
sound_wave = sound_wave + noise

# Convert to 16-bit PCM
audio_data = np.int16(sound_wave * 32767)

# Save as WAV file
with wave.open('sample.wav', 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample (16 bit)
    wav_file.setframerate(framerate)
    wav_file.writeframes(audio_data.tobytes())

print("Created sample.wav")
