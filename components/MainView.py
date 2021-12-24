from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGraphicsDropShadowEffect, QLabel
from PyQt5 import QtWidgets

class cMainView(QWidget):
    def __init__(self, mainwindow, vbox_layout):
        super(cMainView, self).__init__()
        self.vbox_layout = vbox_layout

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        container = QWidget()
        container.setStyleSheet(
            '''
            background: white;
            '''
        )

        self.label = QLabel(container)
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(5);
        effect.setXOffset(0)
        effect.setYOffset(0)
        container.setGraphicsEffect(effect)

        self.label.setText("first label")

        verticalSpacer = QtWidgets.QSpacerItem(
            80, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        hbox.addItem(verticalSpacer)
        hbox.addWidget(container)
        hbox.addItem(verticalSpacer)

        self.vbox_layout.addLayout(hbox)
