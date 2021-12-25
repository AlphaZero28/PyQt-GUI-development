from components.NavigationBar import cNavigationBar
from components.MainView import cMainView
from components.MenuBar import cMenuBar  # custom menubar
from components.ToolBar import cToolBar  # custom toolbar
from components.StatusBar import cStatusBar
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtGui import QIcon

sys.path.append('./components')


class GUIMainWindow(QMainWindow):

    def __init__(self):
        super(GUIMainWindow, self).__init__()

        self.setWindowTitle("Accessible PDF Reader")
        self.setWindowIcon(QIcon('./assets/pdf-reader.png'))
        self.setGeometry(50, 50, 500, 300)

        # Createint a Central Widget to attach the vbox_layout
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
        # initializing STATUS BAR
        self.cstatus_bar = cStatusBar(self)

    def initUI(self):
        self.cmain_view = cMainView(self, self.vbox_layout)
        self.ctool_bar.set_main_view(self.cmain_view)

    def change_label(self, txt):
        self.label.setText(txt)
        self.label.adjustSize()
