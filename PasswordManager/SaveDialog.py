import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 13:53:56 2017

@author: seitz
"""

class SaveDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(SaveDialog, self).__init__(parent)

        # load and show the user interface created with the designer.
        uic.loadUi('../save_dialog.ui', self)

        self.save_button.clicked.connect(self.save)
        self.discard_button.clicked.connect(self.discard)
    
    def save(self):
        self.accept()
    
    def discard(self):
        self.reject()

def _main():
    app = QApplication(sys.argv)
    m = SaveDialog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    _main()
