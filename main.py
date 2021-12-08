from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc 
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTextEdit, \
    QDockWidget, QMessageBox
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()  
        self.setWindowTitle("Aplikasi Sederhana")
        screen = QApplication.primaryScreen().size()
        width = 800 #screen.width()
        height = 600 #screen.height()
        self.setGeometry(0, 0, width,height)
        self.setMaximumSize(width, height)

        # adding a central widget to application:
        self.textEdit = QTextEdit(placeholderText = "Type text here")
        self.setCentralWidget(self.textEdit)

        # add status bar to aplication:
        status_bar = qtw.QStatusBar()
        self.setStatusBar(status_bar)
        # status_bar.showMessage("Welcome to text_editor.py")
        charcount_label = qtw.QLabel("chars: 0")
        self.textEdit.textChanged.connect(lambda: charcount_label.setText("chars: " + 
                                            str(len(self.textEdit.toPlainText()))))
        self.statusBar().addWidget(charcount_label) # or addPermanentWidget()

        # add menus to application:
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        edit_menu = menubar.addMenu('Edit')
        format_menu = menubar.addMenu('Format')
        view_menu = menubar.addMenu('View')
        help_menu = menubar.addMenu('Help')

        # add actions to menu
        new_action = file_menu.addAction('New')
        open_action = file_menu.addAction('Open') 
        save_action = file_menu.addAction('Save')
        sep = file_menu.addSeparator()
        exit_action = file_menu.addAction('Exit', self.close)

        undo_action = edit_menu.addAction('Undo', self.textEdit.undo)

        redo_action = qtw.QAction('Redo', self)
        redo_action.triggered.connect(self.textEdit.redo)
        edit_menu.addAction(redo_action)

        # add toolbar to application:
        toolbar = self.addToolBar('File')
        # open_action = qtw.QAction('Open', self)
        # toolbar.addAction('Save')
        # toolbar.setMovable(False)  
        # toolbar.setFloatable(False)
        file_icon = self.style().standardIcon(qtw.QStyle.SP_FileIcon)
        open_icon = self.style().standardIcon(qtw.QStyle.SP_DirOpenIcon)
        save_icon = self.style().standardIcon(qtw.QStyle.SP_DriveHDIcon)

        new_action.setIcon(file_icon)
        open_action.setIcon(open_icon)
        save_action.setIcon(save_icon)

        toolbar.addAction(open_action)
        # toolbar.addAction(save_icon, 'Save', lambda: self.statusBar().showMessage('File saved!'))
        toolbar.addAction(save_action) 
        save_action.triggered.connect(lambda: self.statusBar().showMessage('File saved!'))

        toolbar.setAllowedAreas(qtc.Qt.TopToolBarArea|qtc.Qt.LeftToolBarArea)
        help_action = qtw.QAction(
            self.style().standardIcon(qtw.QStyle.SP_DialogHelpButton), 
            'Help', 
            self,  
            triggered = lambda: self.statusBar().showMessage('Sorry, no help yet!')
        )
        toolbar.addAction(help_action)
        help_menu.addAction(help_action)

        toolbar2 = qtw.QToolBar('Edit')
        toolbar2.addAction('Copy', self.textEdit.copy)
        toolbar2.addAction('Cut', self.textEdit.cut)
        toolbar2.addAction('Paste', self.textEdit.paste)

        self.addToolBar(qtc.Qt.RightToolBarArea, toolbar2)

        # adding dock widget to application:
        dock = QDockWidget('Replace')
        self.addDockWidget(qtc.Qt.LeftDockWidgetArea, dock)
        dock.setFeatures(qtw.QDockWidget.DockWidgetMovable | qtw.QDockWidget.DockWidgetFloatable)

        # add widget to dock:
        replace_widget = qtw.QWidget() 
        replace_widget.setLayout(qtw.QVBoxLayout())
        dock.setWidget(replace_widget)

        self.search_text_inp = qtw.QLineEdit(placeholderText = 'search')
        self.replace_text_inp = qtw.QLineEdit(placeholderText = 'replace')
        self.search_and_replace_btn = qtw.QPushButton('Search and Replace')
        self.search_and_replace_btn.clicked.connect(self.search_and_replace)

        replace_widget.layout().addWidget(self.search_text_inp)
        replace_widget.layout().addWidget(self.replace_text_inp)
        replace_widget.layout().addWidget(self.search_and_replace_btn)
        replace_widget.layout().addStretch()

        self.show() 
    def search_and_replace(self):
        s_text = self.search_text_inp.text() 
        r_text = self.replace_text_inp.text()  
        
        text = self.textEdit.toPlainText()
        if not s_text in self.textEdit.toPlainText():
            QMessageBox.warning(self, 'Warning', f"{s_text} is not found in the text!")
            
        if s_text:
            text = text.replace(s_text, r_text)
            # self.textEdit.clear()
            self.textEdit.setText(text)
        
        

def window():
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()