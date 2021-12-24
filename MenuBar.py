from PyQt5.QtWidgets import QAction, QFileDialog, QWidget

class cMenuBar(QWidget):
    def __init__(self, mainwindow):
        super(cMenuBar, self).__init__()
        self.mainwindow = mainwindow
        menuBar = self.mainwindow.menuBar()

        # FILE MENU
        fileMenu = menuBar.addMenu('&File')
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.openFiles)
    
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        # exit_action.triggered.connect(lambda: QApplication(sys.argv))

        fileMenu.addAction(open_action)
        fileMenu.addAction(save_action)
        fileMenu.addAction(exit_action)



        # EDIT MENU
        editMenu = menuBar.addMenu('Edit')
        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        
        paste_action = QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
    
        editMenu.addAction(copy_action)
        editMenu.addAction(paste_action)



        # VIEW MENU
        viewMenu = menuBar.addMenu('View')
        zoom_action = QAction('Zoom', self)
    
        Goto_action = QAction('Goto', self)
        
        viewMenu.addAction(zoom_action)
        viewMenu.addAction(Goto_action)


        
        # TOOLS MENU
        toolsMenu = menuBar.addMenu('Tools')



        # HELP MENU
        helpMenu = menuBar.addMenu('Help')
        about_action = QAction('About', self)

        userGuide_action = QAction('User Guide', self)
        
        helpMenu.addAction(about_action)
        helpMenu.addAction(userGuide_action)



    def openFiles(self):
        fname = QFileDialog.getOpenFileName(
            self,'Open File', "")
        self.mainwindow.change_label(fname[0])
