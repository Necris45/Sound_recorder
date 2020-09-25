import sys
from recorder import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = My_window()
    w.resize(300, 50)
    w.setWindowTitle('Sound_recorder')
    w.show()

sys.exit(app.exec_())
