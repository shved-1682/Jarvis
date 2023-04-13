import json

import pyaudio
from vosk import KaldiRecognizer, Model


class Recognition:
    __sample_format = pyaudio.paInt16  # 16 бит на выборку
    channels = 1
    rate = 16_000  # Запись со скоростью 1600 выборок(samples) в секунду
    chunk = 8_000  # Запись кусками по 1024 сэмпла

    def __init__(self, path: str):
        self.__p = pyaudio.PyAudio()  # Create interface for PortAudio
        self.model = Model(path)
        self.__rec = KaldiRecognizer(self.model, 16_000)
        self.stream = self.__p.open(
            format=self.__sample_format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            input_device_index=0,  # индекс устройства с которого будет идти запись звука 
        )
        self.stream.start_stream()

    def listen(self):
        while True:
            data = self.stream.read(
                4000,
                exception_on_overflow=False
            )
            if (self.__rec.AcceptWaveform(data)) and (len(data) > 0):
                answer = json.loads(self.__rec.Result())
                if answer['text']:
                    yield answer['text']
