# from curses import ACS_DARROW
import sys
from PyQt5.QtWidgets import QApplication
from GUIMain import GUIMainWindow
# ACS_DARROW
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GUIMainWindow()
    
    win.show()
    sys.exit(app.exec_())
