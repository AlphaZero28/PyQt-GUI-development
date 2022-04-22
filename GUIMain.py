from components.NavigationBar import cNavigationBar
from components.MainView import cMainView
from components.MenuBar import cMenuBar  # custom menubar
from components.ToolBar import cToolBar  # custom toolbar
from components.StatusBar import cStatusBar
from components.ContextMenu import cContextMenu
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5.QtGui import QIcon

sys.path.append('./components')


class GUIMainWindow(QMainWindow):

    def __init__(self, file_intent):
        super(GUIMainWindow, self).__init__()
        self.file_intent = file_intent
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

        self.cmain_view.start_work() # cmain_view is functioning, any processes can be now started

        self.installEventFilter(self)

    # def keyPressEvent(self, event):
    #     print(event.key())
    #     if event.key() == QtCore.Qt.Key_D:
    #         self.cmain_view.goto_next_page()
    #     elif event.key() == QtCore.Qt.Key_A:
    #         self.cmain_view.goto_prev_page()

    def eventFilter(self, source, event):
        # print(event)
        if event.type() == 51: # QKeyEvent
            if event.key() == 16777234: # left arrow
                print('left arrow key press')
                self.cmain_view.goto_prev_page()
            elif event.key() == 16777236: # right arrow
                print('right arrow key press')
                self.cmain_view.goto_next_page()
            elif event.key() == 16777235: # up arrow
                print('up arrow key press')
                self.cmain_view.up_arrow_press()
            elif event.key() == 16777237: # down arrow
                print('down arrow key press')
                self.cmain_view.down_arrow_press()
                
        return super(GUIMainWindow, self).eventFilter(source, event)

    def initUI(self):
        self.cmain_view = cMainView(self, self.vbox_layout, self.file_intent)
        self.ctool_bar.set_main_view(self.cmain_view)
        self.cmenu_bar.set_main_view(self.cmain_view)
        # self.navigation_bar.set_main_view(self.cmain_view)

    def change_label(self, txt):
        self.label.setText(txt)
        self.label.adjustSize()
