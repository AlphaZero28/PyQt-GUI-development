from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QIcon


class cNavigationBar(QWidget):
    def __init__(self, mainwindow, vbox_layout):
        super(cNavigationBar, self).__init__()
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)

        zoom_level = QLabel('100%')
        left_btn = QPushButton()
        left_btn.setFlat(True)
        left_btn.setIcon(QIcon('./assets/left-arrow.png'))

        right_btn = QPushButton()
        right_btn.setFlat(True)
        right_btn.setIcon(QIcon('./assets/right-arrow.png'))
        right_btn.clicked.connect(self.nextPage)

        hlayout.addWidget(left_btn, 0)
        hlayout.addWidget(right_btn, 0)
        hlayout.addWidget(zoom_level, 1)

        # qW = QWidget()
        # # qW.setStyleSheet('border: 3px solid gray;margin-top:0px')
        # qW.setLayout(hlayout)

        # # vbox_layout.addWidget(qW,0)
        vbox_layout.addLayout(hlayout)

    def nextPage(self):
        test = 'test start'

        self.cmain_view.get_nextPage(test)

    def set_main_view(self, cmain_view):
        self.cmain_view = cmain_view
