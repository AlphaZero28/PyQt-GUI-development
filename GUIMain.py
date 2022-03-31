from components.NavigationBar import cNavigationBar
from components.MainView import cMainView
from components.MenuBar import cMenuBar  # custom menubar
from components.ToolBar import cToolBar  # custom toolbar
from components.StatusBar import cStatusBar
from components.ContextMenu import cContextMenu
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtGui import QIcon

sys.path.append('./components')


class GUIMainWindow(QMainWindow):

    def __init__(self):
        super(GUIMainWindow, self).__init__()
        self.showMaximized()

        self.setWindowTitle("Pathak")
        self.setWindowIcon(QIcon('./assets/pdf-reader.png'))

        width = QtWidgets.QDesktopWidget().screenGeometry().width()
        height = QtWidgets.QDesktopWidget().screenGeometry().height()
        # width = 400
        # height = 500
        self.setGeometry(0, 0, width, height)
        # self.setMinimumSize(400,500)
        # Createint a Central Widget to attach the vbox_layout
        # self.central_widget = QtWidgets.QWidget()
        self.central_widget = QtWidgets.QWidget()

        self.setCentralWidget(self.central_widget)

        # vbox_layout will contain the cMainView elements
        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.setContentsMargins(0, 0, 0, 0)
        self.vbox_layout.setSpacing(0)
        
        self.central_widget.setLayout(self.vbox_layout)

        # initializing MENUBAR and TOOLBAR
        self.cmenu_bar = cMenuBar(self)
        self.ctool_bar = cToolBar(self)
        

        # initializing main windows UI
        self.initUI()

        self.navigation_bar = cNavigationBar(self, self.vbox_layout)
        self.navigation_bar.set_main_view(self.cmain_view)

        # initializing STATUS BAR
        self.cstatus_bar = cStatusBar(self)

        self.cmain_view.set_status_bar(self.cstatus_bar)

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == QtCore.Qt.Key_D:
            self.cmain_view.goto_next_page()
        elif event.key() == QtCore.Qt.Key_A:
            self.cmain_view.goto_prev_page()

    def initUI(self):
        self.cmain_view = cMainView(self, self.vbox_layout)
        self.ctool_bar.set_main_view(self.cmain_view)
        self.cmenu_bar.set_main_view(self.cmain_view)
        # self.navigation_bar.set_main_view(self.cmain_view)

    def change_label(self, txt):
        self.label.setText(txt)
        self.label.adjustSize()
