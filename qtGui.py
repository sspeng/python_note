#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class Form(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        nameLabel = QtWidgets.QLabel()
        self.nameLine = QtWidgets.QLineEdit()
        self.submitButton = QtWidgets.QPushButton("&Submit")

        buttonLayout1 = QtWidgets.QVBoxLayout()
        buttonLayout1.addWidget(nameLabel)
        buttonLayout1.addWidget(self.nameLine)
        buttonLayout1.addWidget(self.submitButton)

        self.submitButton.clicked.connect(self.submitContact)
        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addLayout(buttonLayout1, 0, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Hello")

    @pyqtSlot()
    def submitContact(self):
        name = self.nameLine.text()

        if name == "":
            QtWidgets.QMessageBox.information(self, "Empty field",
                                              "Please enter a name and address.")
            return
        else:
            QtWidgets.QMessageBox.information(self, "Success!", "Hello %s!" % name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    screen = Form()
    screen.show()

    sys.exit(app.exec())