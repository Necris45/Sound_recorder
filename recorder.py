import pyaudio
import wave
from pyaudio import Stream
from pydub import AudioSegment
from PyQt5.QtWidgets import *

chunk = 1024  # Запись кусками по 1024 сэмпла
sample_format = pyaudio.paInt16  # 16 бит на выборку
channels = 2
rate = 44100  # Запись со скоростью 44100 выборок(samples) в секунду
seconds = 10
filename1 = "input_sound.wav"
filename2 = "output_sound.wav"


def stop_record():
    # Остановить и закрыть поток
    stream1.stop_stream()
    stream2.stop_stream()
    stream1.close()
    stream2.close()
    # Завершить интерфейс PortAudio
    p.terminate()


def save_sound():
    # Сохранить записанные данные в виде файла wav
    wf1 = wave.open(filename1, 'wb')
    wf1.setnchannels(channels)
    wf1.setsampwidth(p.get_sample_size(sample_format))
    wf1.setframerate(rate)
    wf1.writeframes(b''.join(frames1))
    wf1.close()
    if len(frames2) > 0:
        wf2 = wave.open(filename2, 'wb')
        wf2.setnchannels(channels)
        wf2.setsampwidth(p.get_sample_size(sample_format))
        wf2.setframerate(rate)
        wf2.writeframes(b''.join(frames2))
        wf2.close()
    # Объединяем имеющиеся wav файлы в единый mp3 файл
    sound1 = AudioSegment.from_file("input_sound.wav", format="wav")
    sound2 = AudioSegment.from_file("output_sound.wav", format="wav")
    sound = sound1.overlay(sound2)
    sound.export("mixin.mp3", format='mp3')


class Recorder(QWidget):

    chunk = 1024  # Запись кусками по 1024 сэмпла
    sample_format = pyaudio.paInt16  # 16 бит на выборку
    channels = 2
    rate = 44100  # Запись со скоростью 44100 выборок(samples) в секунду
    seconds = 10

    def __init__(self):
        QWidget.__init__(self)
        self.drop1 = QComboBox(self)
        self.drop1.addItems(["Запись только с микрофона", "Запись всего звука"])
        self.drop1.show()
        self.button1 = QPushButton(self)
        self.button1.move(180, 0)

    def record(self):
        p = pyaudio.PyAudio()  # Создать интерфейс для PortAudio
        stream1 = p.open(format=sample_format,
                         channels=channels,
                         rate=rate,
                         frames_per_buffer=chunk,
                         input_device_index=2,  # индекс устройства с которого будет идти запись звука (микрофон)
                         input=True)
        if self.drop1.currentText() != "Запись только с микрофона":
            stream2 = p.open(format=sample_format,
                             channels=channels,
                             rate=rate,
                             frames_per_buffer=chunk,
                             input_device_index=1,  # индекс устройства с которого будет идти запись (стереомикшер)
                             input=True)
        frames1 = []  # Инициализировать массив для хранения данных с микрофона
        frames2 = []  # Инициализировать массив для хранения данных с стереомикшера
        if self.drop1.currentText() != "Запись только с микрофона":
            for i in range(0, int(rate / chunk * seconds)):
                data1 = stream1.read(chunk)
                frames1.append(data1)
                data2 = stream2.read(chunk)
                frames2.append(data2)
            else:
                data1 = stream1.read(chunk)
                frames1.append(data1)
