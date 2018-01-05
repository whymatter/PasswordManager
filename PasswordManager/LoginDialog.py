import sys
import os.path
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from Crypto.Cipher import AES
import json

from constants import FILE_NAME, KEY_ENCODING
from PwWindow import PwWindow

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 13:53:56 2017

@author: seitz
"""

class LoginDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, key=None):
        super(LoginDialog, self).__init__(parent)
        self.pw_window = None

        # load and show the user interface created with the designer.
        uic.loadUi('../login_dialog.ui', self)

        self.login_button.clicked.connect(self.login)
        self.show()
    
    def get_key(self):
        return self.key_lineedit.text().encode(KEY_ENCODING)

    def login(self):
        if not os.path.isfile(FILE_NAME):
            cipher = AES.new(self.get_key(), AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(json.dumps([]).encode(KEY_ENCODING))
            
            with open(FILE_NAME, "wb") as file_out:
                [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]

        if self.load_data(FILE_NAME, self.get_key()):
            self.hide()
            self.pw_window = PwWindow(key=self.get_key()) 

    def load_data(self, filename, key):
        try:
            with open(filename, 'rb') as file_in:
                print(file_in)
                nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
                
                # let's assume that the key is somehow available again
                cipher = AES.new(key, AES.MODE_EAX, nonce)
                jsontext = cipher.decrypt_and_verify(ciphertext, tag)
                data = json.loads(jsontext)
                return True
        except Exception as e:
            print("Your file contains errors")
            print(e)
            return False

def _main():
    app = QApplication(sys.argv)
    m = LoginDialog()
    sys.exit(app.exec_())


if __name__ == '__main__':
    _main()
