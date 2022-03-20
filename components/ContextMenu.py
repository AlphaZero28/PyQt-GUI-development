from PyQt5.QtWidgets import QMainWindow, QWidget, QTreeView
from PyQt5 import QtCore, Qt, QtGui
# from PyQt5.QtGui import QTreeView

# from QWidget import centralWidget

class cContextMenu(QWidget):
    def __init__(self, mainwindow,vbox_layout):
        super(cContextMenu, self).__init__()
        self.mainwindow = mainwindow
        self.vbox_layout = vbox_layout

        # tree view
        self.tree = QTreeView()
        self.vbox_layout.addWidget(self.tree)


        # self.centralWidget.setContextMenuPolicy()
        # self.centralWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

        # self.centralWidget.addAction(self.openAction)
        # self.centralWidget.addAction(self.saveAction)
        # self.centralWidget.addAction(self.exitAction)

        # def contextMenuEvent(self,event):
        #     contextMenu = QMenu(self)
        #     openAct = contextMenu.addAction("open")
        #     saveAct = contextMenu.addAction("save")
        #     exitAct = contextMenu.addAction("exit")

        #     action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        #     if action == quitAct:
        #         self.close()
