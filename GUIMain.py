import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtGui import QIcon
from components.StatusBar import cStatusBar
from components.ToolBar import cToolBar  # custom toolbar
from components.MenuBar import cMenuBar  # custom menubar
from components.MainView import cMainView
sys.path.append('./components')

<<<<<<< HEAD
=======
from StatusBar import cStatusBar
from ToolBar import cToolBar  # custom toolbar
from MenuBar import cMenuBar  # custom menubar
from MainView import cMainView
from NavigationBar import cNavigationBar
>>>>>>> d1eda0a236222cc3defab6f91bcc07cea533a2ea

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
        self.cMain_View = cMainView(self, self.vbox_layout)

        # initializing main windows UI
        # self.initUI()

        self.navigation_bar = cNavigationBar(self,self.vbox_layout)
        # initializing STATUS BAR
        self.cstatus_bar = cStatusBar(self)

<<<<<<< HEAD
    # def initUI(self):
    #     cMainView(self, self.vbox_layout)
=======

    def initUI(self):
        cMainView(self, self.vbox_layout)

>>>>>>> d1eda0a236222cc3defab6f91bcc07cea533a2ea
    def change_label(self, txt):
        self.label.setText(txt)
        self.label.adjustSize()
