import pyaudio
import wave

chunk = 1024  # Запись кусками по 1024 сэмпла
sample_format = pyaudio.paInt16  # 16 бит на выборку
channels = 2
rate = 44100  # Запись со скоростью 44100 выборок(samples) в секунду
seconds = 5
filename1 = "input_sound.wav"
filename2 = "output_sound.wav"
p = pyaudio.PyAudio()  # Создать интерфейс для PortAudio

print('Recording...')

stream1 = p.open(format=sample_format,
                 channels=channels,
                 rate=rate,
                 frames_per_buffer=chunk,
                 input_device_index=1,  # индекс устройства с которого будет идти запись звука
                 input=True)

stream2 = p.open(format=sample_format,
                 channels=channels,
                 rate=rate,
                 frames_per_buffer=chunk,
                 input_device_index=3,  # индекс устройства с которого будет идти запись звука
                 as_loopback=True)

frames1 = []  # Инициализировать массив для хранения
frames2 = []  # Инициализировать массив для хранения

# Хранить данные в блоках в течение 3 секунд
for i in range(0, int(rate / chunk * seconds)):
    data1 = stream1.read(chunk)
    data2 = stream2.read(chunk)
    frames1.append(data1)
    frames2.append(data2)

# Остановить и закрыть поток
stream1.stop_stream()
stream2.stop_stream()
stream1.close()
stream2.close()
# Завершить интерфейс PortAudio
p.terminate()

print('Finished recording!')

# Сохранить записанные данные в виде файла wav
wf1 = wave.open(filename1, 'wb')
wf2 = wave.open(filename2, 'wb')
wf1.setnchannels(channels)
wf2.setnchannels(channels)
wf1.setsampwidth(p.get_sample_size(sample_format))
wf2.setsampwidth(p.get_sample_size(sample_format))
wf1.setframerate(rate)
wf2.setframerate(rate)
wf1.writeframes(b''.join(frames1))
wf2.writeframes(b''.join(frames2))
wf1.close()
wf2.close()
