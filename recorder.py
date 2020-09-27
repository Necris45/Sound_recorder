import pyaudio
import wave
from PyQt5.QtCore import pyqtSignal
from pydub import AudioSegment
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import time


class Recorder(QtCore.QObject):
    rec_start = 0
    chunk = 1024  # Запись кусками по 1024 сэмпла
    sample_format = pyaudio.paInt16  # 16 бит на выборку
    channels = 2
    rate = 44100  # Запись со скоростью 44100 выборок(samples) в секунду
    filename1 = "device1_sound.wav"
    filename2 = "device2_sound.wav"
    p = pyaudio.PyAudio()  # Создать интерфейс для PortAudio
    frames1 = []  # Инициализировать массив для хранения данных с микрофона
    frames2 = []  # Инициализировать массив для хранения данных с стереомикшера
    finished = pyqtSignal()
    current_time = ''
    device_used = 0
    device1_index = 0
    device2_index = 0

    # метод, который будет выполнять алгоритм в другом потоке
    def run(self):
        self.current_time = str(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))
        if self.device_used == 2:
            stream1 = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  frames_per_buffer=self.chunk,
                                  # индекс устройства с которого будет идти запись звука
                                  input_device_index=self.device1_index,
                                  input=True)
            stream2 = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  frames_per_buffer=self.chunk,
                                  # индекс устройства с которого будет идти запись звука
                                  input_device_index=self.device2_index,
                                  input=True)
            while self.rec_start == 1:
                data1 = stream1.read(self.chunk)
                self.frames1.append(data1)
                data2 = stream2.read(self.chunk)
                self.frames2.append(data2)
            stream1.stop_stream()
            stream2.stop_stream()
        elif self.device_used == 1:
            stream1 = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  frames_per_buffer=self.chunk,
                                  # индекс устройства с которого будет идти запись звука
                                  input_device_index=self.device1_index,
                                  input=True)
            while self.rec_start == 1:
                data1 = stream1.read(self.chunk)
                self.frames1.append(data1)
            stream1.stop_stream()
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
        if self.device_used == 2:
            sound1 = AudioSegment.from_file(self.filename1, format="wav")
            sound2 = AudioSegment.from_file(self.filename2, format="wav")
            sound = sound1.overlay(sound2)
            sound.export(('{}.mp3'.format(self.current_time)), format='mp3')
        elif self.device_used == 1:
            sound = AudioSegment.from_file(self.filename1, format="wav")
            sound.export(('{}.mp3'.format(self.current_time)), format='mp3')
        self.frames1.clear()
        self.frames2.clear()
        self.finished.emit()


class My_window(QWidget):
    def __init__(self):
        # определяем список доступных устройств
        self.p1 = pyaudio.PyAudio()
        host_info = self.p1.get_host_api_info_by_index(0)
        device_count = host_info.get('deviceCount')
        self.devices = list()
        self.devices_dict = {}
        # заполняем словарь и список устройств:
        for i in range(0, device_count):
            device = self.p1.get_device_info_by_host_api_device_index(0, i)
            self.devices.append(device['name'])
            key = device['name']
            index = device['index']
            self.devices_dict[key] = index
        QWidget.__init__(self)
        # создадим поток
        self.thread = QtCore.QThread()
        # создадим объект для выполнения кода в другом потоке
        self.record = Recorder()
        # перенесём объект в другой поток
        self.record.moveToThread(self.thread)
        # подключим сигнал старта потока к методу run у объекта, который должен выполнять код в другом потоке
        self.thread.started.connect(self.record.run)
        self.label1 = QLabel(self)
        self.label1.setText('Выбирете микрофон')
        self.label1.setGeometry(5, 5, 150, 13)
        self.label2 = QLabel(self)
        self.label2.setText('Выбирете стереомикшер')
        self.label2.setGeometry(155, 5, 150, 13)
        self.drop1 = QComboBox(self)
        self.drop1.addItems(self.devices)
        self.drop1.setGeometry(5, 20, 145, 20)
        self.drop1.show()
        self.drop2 = QComboBox(self)
        self.drop2.addItems(self.devices)
        self.drop2.setGeometry(155, 20, 145, 20)
        self.drop2.show()
        self.drop3 = QComboBox(self)
        self.drop3.addItems(["Запись с первого устройства", "Запись с двух устройств"])
        self.drop3.setGeometry(5, 50, 170, 20)
        self.drop3.show()
        self.label3 = QLabel(self)
        self.label3.setText('Нажмите кнопку для записи')
        self.label3.setGeometry(5, 75, 180, 26)
        self.button1 = QPushButton(self)
        self.button1.setGeometry(180, 50, 60, 50)
        self.button1.setText('запись')
        self.button2 = QPushButton(self)
        self.button2.setGeometry(242, 50, 60, 50)
        self.button2.setText('Стоп')
        self.button2.setEnabled(False)
        self.button1.clicked.connect(self.rec)
        self.button2.clicked.connect(self.stop)
        self.record.finished.connect(self.done)

    def rec(self):
        self.button1.setEnabled(False)
        self.drop1.setEnabled(False)
        self.drop2.setEnabled(False)
        self.drop3.setEnabled(False)
        self.button2.setEnabled(True)
        self.record.rec_start = 1
        self.record.device1_index = self.devices_dict[self.drop1.currentText()]
        self.record.device2_index = self.devices_dict[self.drop2.currentText()]
        if self.drop3.currentText() == "Запись с первого устройства":
            self.record.device_used = 1
        else:
            self.record.device_used = 2
        self.thread.start()
        self.label3.setText('Идет запись\nДля остановки нажми Стоп')

    def stop(self):
        self.record.rec_start = 0
        self.button2.setEnabled(False)

    def done(self):
        self.thread.quit()
        self.thread.wait(1000)
        self.button1.setEnabled(True)
        self.drop1.setEnabled(True)
        self.drop2.setEnabled(True)
        self.drop3.setEnabled(True)
        self.label3.setText('Запись завершена и сохранена\nНажмите кнопку для записи')
