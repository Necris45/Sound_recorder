import sys
import pyaudio
import wave
from pydub import AudioSegment
from PyQt5.QtWidgets import *
from recorder import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Recorder()
    w.resize(300, 25)
    w.setWindowTitle('Sound_recorder')
    w.show()

sys.exit(app.exec_())
