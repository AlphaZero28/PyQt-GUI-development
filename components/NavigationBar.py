from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QIcon


class cNavigationBar(QWidget):
    def __init__(self, mainwindow, vbox_layout):
        super(cNavigationBar, self).__init__()
        # self.mainwindow = mainwindow
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)

        zoom_level = QLabel('100%')
        left_btn = QPushButton()
        left_btn.setFlat(True)
        left_btn.setIcon(QIcon('./assets/left-arrow.png'))
        left_btn.clicked.connect(self.prev_page)

        right_btn = QPushButton()
        right_btn.setFlat(True)
        right_btn.setIcon(QIcon('./assets/right-arrow.png'))
        right_btn.clicked.connect(self.next_page)

        hlayout.addWidget(left_btn, 0)
        hlayout.addWidget(right_btn, 0)
        hlayout.addWidget(zoom_level, 1)

        # qW = QWidget()
        # # qW.setStyleSheet('border: 3px solid gray;margin-top:0px')
        # qW.setLayout(hlayout)

        # # vbox_layout.addWidget(qW,0)
        vbox_layout.addLayout(hlayout)

    def next_page(self):
        self.cmain_view.goto_next_page()
    
    def prev_page(self):
        self.cmain_view.goto_prev_page()

    def set_main_view(self, cmain_view):
        self.cmain_view = cmain_view
