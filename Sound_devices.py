import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(i, p.get_device_info_by_index(i)['name'])

# detect devices:
# p = pyaudio.PyAudio()
host_info = p.get_host_api_info_by_index(0)
device_count = host_info.get('deviceCount')
devices = []

# iterate between devices:
for i in range(0, device_count):
    device = p.get_device_info_by_host_api_device_index(0, i)
    devices.append(device['name'])

print(devices)
