import sys
from PyQt5.QtWidgets import QApplication
from GUIMain import GUIMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GUIMainWindow()
    
    win.show()
    sys.exit(app.exec_())
