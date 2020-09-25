import pyaudio
import wave

from PyQt5.QtCore import pyqtSignal
from pyaudio import Stream
from pydub import AudioSegment
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import time


class Recorder(QtCore.QObject):
    running = False
    x = 0
    chunk = 1024  # Запись кусками по 1024 сэмпла
    sample_format = pyaudio.paInt16  # 16 бит на выборку
    channels = 2
    rate = 44100  # Запись со скоростью 44100 выборок(samples) в секунду
    seconds = 10
    filename1 = "input_sound.wav"
    filename2 = "output_sound.wav"
    p = pyaudio.PyAudio()  # Создать интерфейс для PortAudio
    stream1 = p.open(format=sample_format,
                     channels=channels,
                     rate=rate,
                     frames_per_buffer=chunk,
                     input_device_index=1,  # индекс устройства с которого будет идти запись звука (микрофон)
                     input=True)
    stream2 = p.open(format=sample_format,
                     channels=channels,
                     rate=rate,
                     frames_per_buffer=chunk,
                     input_device_index=2,  # индекс устройства с которого будет идти запись (стереомикшер)
                     input=True)
    stream1.stop_stream()
    stream2.stop_stream()
    frames1 = []  # Инициализировать массив для хранения данных с микрофона
    frames2 = []  # Инициализировать массив для хранения данных с стереомикшера
    finished = pyqtSignal()

    # метод, который будет выполнять алгоритм в другом потоке
    def run(self):
        self.x = 1
        self.stream1.start_stream()
        self.stream2.start_stream()
        while self.x == 1:
            # for i in range(0, int(self.rate / self.chunk * self.seconds)):
            data1 = self.stream1.read(self.chunk)
            self.frames1.append(data1)
            data2 = self.stream2.read(self.chunk)
            self.frames2.append(data2)
        self.stream1.stop_stream()
        self.stream2.stop_stream()
        # self.stream1.close()
        # self.stream2.close()
        # Завершить интерфейс PortAudio
        # self.p.terminate()
        # Сохранить записанные данные в виде файла wav
        wf1 = wave.open(self.filename1, 'wb')
        wf1.setnchannels(self.channels)
        wf1.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf1.setframerate(self.rate)
        wf1.writeframes(b''.join(self.frames1))
        wf1.close()
        if len(self.frames2) > 0:
            wf2 = wave.open(self.filename2, 'wb')
            wf2.setnchannels(self.channels)
            wf2.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf2.setframerate(self.rate)
            wf2.writeframes(b''.join(self.frames2))
            wf2.close()
        # Объединяем имеющиеся wav файлы в единый mp3 файл
        sound1 = AudioSegment.from_file(self.filename1, format="wav")
        sound2 = AudioSegment.from_file(self.filename2, format="wav")
        sound = sound1.overlay(sound2)
        sound.export("mixin.mp3", format='mp3')
        self.frames1.clear()
        self.frames2.clear()
        self.finished.emit()


class My_window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # создадим поток
        self.thread = QtCore.QThread()
        # создадим объект для выполнения кода в другом потоке
        self.record = Recorder()
        # перенесём объект в другой поток
        self.record.moveToThread(self.thread)
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread.started.connect(self.record.run)
        self.drop1 = QComboBox(self)
        self.drop1.addItems(["Запись только с микрофона", "Запись всего звука"])
        self.drop1.show()
        self.label1 = QLabel(self)
        self.label1.setText('Нажмите кнопку для записи')
        self.label1.setGeometry(5, 25, 180, 13)
        self.button1 = QPushButton(self)
        self.button1.setGeometry(180, 0, 50, 50)
        self.button1.setText('запись')
        self.button2 = QPushButton(self)
        self.button2.setGeometry(233, 0, 50, 50)
        self.button2.setText('Стоп')
        self.button1.clicked.connect(self.rec)
        self.button2.clicked.connect(self.stop)
        self.record.finished.connect(self.done)

    def rec(self):
        self.thread.start()

    def stop(self):
        self.record.x = 0

    def done(self):
        self.thread.quit()
        self.thread.wait(1000)
        print('stopped')
