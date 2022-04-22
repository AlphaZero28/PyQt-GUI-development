# from curses import ACS_DARROW
import sys
from PyQt5.QtWidgets import QApplication
from GUIMain import GUIMainWindow
# ACS_DARROW
if __name__ == '__main__':

    file_intent = ''
    if len(sys.argv)>1:
        if sys.argv[1].endswith('.pdf'): #only open pdf
            file_intent = sys.argv[1] # intent to open file with 'open with'

    app = QApplication(sys.argv)
    win = GUIMainWindow(file_intent)
    
    win.show()
    sys.exit(app.exec_())
