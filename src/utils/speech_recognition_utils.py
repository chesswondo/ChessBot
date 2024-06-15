import pyaudio
import wave

def record_audio(filename: str, duration: int, sample_rate: int, channels: int) -> None:
    """
    Records and saves audio file from microphone.

    : param filename: (str) - filename to save.
    : param duration: (int) - duration of a single audio.
    : param sample_rate: (int) - sample rate of an audio file.
    : param channels: (int) - number of channels to write.
    
    : return: (None) - this function does not return any value.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=1024)
    frames = []
    
    print("Recording...")
    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    print("Finished recording.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()