import sounddevice as sd

SAMPLE_RATE = 16000

def record(seconds=4):
    print(f"Listening for {seconds}s... bolo!")
    audio = sd.rec(int(seconds * SAMPLE_RATE),
                   samplerate=SAMPLE_RATE,
                   channels=1,
                   dtype="float32")
    sd.wait()
    return audio.flatten()