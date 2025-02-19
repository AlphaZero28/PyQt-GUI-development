from PyQt5.QtWidgets import QStatusBar, QWidget, QLabel
from PyQt5.QtGui import QFont

class cStatusBar(QWidget):
    def __init__(self, mainwindow):
        super(cStatusBar, self).__init__()
        self.statusBar = QStatusBar()
        mainwindow.setStatusBar(self.statusBar)

        # self.label = QLabel(self.statusBar)
        # self.label.setText('hi')
        self.show_msg('hello')
        
        self.statusBar.setFont(QFont('SansSerif', 7))
        self.statusBar.setStyleSheet('''
            QStatusBar {
                border:2px solid rgba(220,220,220,0.6);
                background: white;
            }
        ''')

    def show_msg(self, msg):
        # self.label.setText(msg)
        # self.label.setFocus()
        self.statusBar.showMessage(msg)
        self.statusBar.setFocus()

        

        