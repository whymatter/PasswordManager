import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from Crypto.Cipher import AES
import json

from constants import FILE_NAME, KEY_ENCODING
from SaveDialog import SaveDialog

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 13:53:56 2017

@author: seitz
"""

class PwWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None, key=None):
        super(PwWindow, self).__init__(parent)
        self.key = key
        self.save_dialog = SaveDialog(parent=self)

        # load and show the user interface created with the designer.
        uic.loadUi('../pw_window.ui', self)

        self.add_button.clicked.connect(self.add_row)
        self.remove_button.clicked.connect(self.remove_row)
        self.toggle_button.clicked.connect(self.toggle_password)
        
        self.load_data(FILE_NAME, key)
        
        self.show()

    def add_row(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())

    def remove_row(self):
        self.tableWidget.removeRow(self.tableWidget.currentRow())
    
    def toggle_password(self):
        item = self.tableWidget.currentItem()
        if item == None or item.column() != 1:
            return
        print(item.text())
        print(item.text() == '****')
        if item.text() == '****':
            print(str(item.data(1)))
            item.setText(str(item.data(1)))
        else:
            item.setData(1, item.text())
            item.setText('****')
        
    def closeEvent(self, event):
        if self.save_dialog.exec_():
            self.save_data(FILE_NAME, self.key)
        
        event.accept()

    def get_data(self):
        data = []
        
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 0) == None or\
               self.tableWidget.item(row, 1) == None:
                continue
            
            data_pw = self.tableWidget.item(row, 1).data(1)
            text_pw = self.tableWidget.item(row, 1).text()
            print(data_pw)
            data.append({
                    
                "accountid": self.tableWidget.item(row, 0).text(),
                "password": text_pw if text_pw != '****' else data_pw
            })

        return data

    def load_data(self, filename, key):
        try:
            with open(filename, 'rb') as file_in:
                nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
                
                # let's assume that the key is somehow available again
                cipher = AES.new(key, AES.MODE_EAX, nonce)
                jsontext = cipher.decrypt_and_verify(ciphertext, tag)
                data = json.loads(jsontext)
                print(data)
                self.refresh_table(data)
        except Exception as e:
            print("Your file contains errors")
            print(e)
            
    def save_data(self, filename, key):
        data = self.get_data()
        print(data)
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(json.dumps(data).encode(KEY_ENCODING))
            
        try:
            with open(FILE_NAME, "wb") as file_out:
                [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
        except Exception as e:
            print("Your file contains errors")
            print(e)

    def refresh_table(self, data):
        def load_value(row, column, value):
            self.tableWidget.setItem(row, column, QTableWidgetItem(str(value), 0))

        [self.tableWidget.removeRow(0) for x in range(self.tableWidget.rowCount())]
        for index, entry in enumerate(data):
            self.tableWidget.insertRow(index)
            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(entry['accountid']), 0))
            pw_item = QTableWidgetItem()
            pw_item.setText('****')
            
            pw_item.setData(1, str(entry['password']))
            self.tableWidget.setItem(index, 1, pw_item)

    @staticmethod
    def persist(data, filename):
        try:
            print(data)
            with open(filename, 'w') as outFile:
                json.dump(data, outFile)
        except Exception as e:
            print("Failed to save!")
            print(e)

    def return_data(self):
        self.data = self.get_data()
        self.accept()

def _main():
    app = QApplication(sys.argv)
    m = PwWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    _main()
