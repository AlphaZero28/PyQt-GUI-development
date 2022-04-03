from PyQt5.QtWidgets import QAction, QFileDialog, QWidget,QApplication,QLabel
import sys 
from components.ImageProcessing import imgProcess
from components.config import DEBUG

class cMenuBar(QWidget):
    def __init__(self, mainwindow):
        super(cMenuBar, self).__init__()
        self.mainwindow = mainwindow
        menuBar = self.mainwindow.menuBar()

        # FILE MENU
        fileMenu = menuBar.addMenu('&File')
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open A File')
        open_action.triggered.connect(self.openFiles)
    
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.saveFiles)

        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        # exit_action.triggered.connect(lambda: sys.exit(app.exec_())))

        fileMenu.addAction(open_action)
        fileMenu.addAction(save_action)
        fileMenu.addSeparator()
        fileMenu.addAction(exit_action)



        # EDIT MENU
        editMenu = menuBar.addMenu('Edit')
        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        line = QLabel()
        copy_action.setStatusTip('Copy a text')
        # copy_action.triggered.connect(self.copyContent(line))

        def copyContent(line):
            cb = QApplication.clipboard()
            cb.clear(mode = cb.clipboard)
            cb.setText(line.text(), mode = cb.clipboard)
            
        
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

    def set_main_view(self, cmain_view):
        self.cmain_view = cmain_view

        
    def openFiles(self):
        self.mainwindow.ctool_bar.openFiles()

    def saveFiles(self):
        self.mainwindow.ctool_bar.saveFiles()

        # fname = QFileDialog.getOpenFileName(
        #     self, 'Open File', "", "PDF files (*.pdf);;")
        
        # if fname[0]=='':
        #     return

        # print('fname',fname)
        # imgs = imgProcess.get_pages(fname[0])
        # self.cmain_view.set_imgs(imgs)
