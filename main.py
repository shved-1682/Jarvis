import json

import pyaudio
from vosk import KaldiRecognizer, Model


def main():
    model = Model("./voice_models/vosk-model-ru-0.10")
    rec = KaldiRecognizer(model, 16_000)
    p = pyaudio.PyAudio()  # Create interface for PortAudio

    sample_format = pyaudio.paInt16 # 16 бит на выборку
    channels = 1
    rate = 16_000 # Запись со скоростью 1600 выборок(samples) в секунду
    chunk = 8_000 # Запись кусками по 1024 сэмпла
    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk,
        input_device_index=0,  # индекс устройства с которого будет идти запись звука 
    )
    stream.start_stream()

    def listen():
        while True:
            data = stream.read(
                4000,
                exception_on_overflow=False
            )
            if (rec.AcceptWaveform(data)) and (len(data) > 0):
                answer = json.loads(rec.Result())
                if answer['text']:
                    yield answer['text']
    
    print('Start listening...')
    for text in listen():
        text_words = text.split(" ")
        if text_words[0] == "джарвис":
            text = " ".join(text_words[1:])
            if text in ["пока", "досвидание", "удачи"]:
                print("Досвидание")
                quit()
            print(text)


if __name__ == "__main__":
    main()
