#! /usr/bin/python3
#  -*- coding: utf8 -*-

import sys
from  PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLCDNumber, QSlider, QVBoxLayout, QApplication


class SigSlot(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.setWindowTitle("XXOO")
        lcd = QLCDNumber(self)
        slider = QSlider(Qt.Horizontal, self)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(slider)

        self.setLayout(vbox)
        """ 
            connect signal with slot
            silder.valueChanged is signal 
            lcd.display is the slot
            silder emit a valuechanged signal 
            when user change the silder
            lcd receive the signal and change 
            the display value
        """

        slider.valueChanged.connect(lcd.display)
        self.resize(350, 250)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qb = SigSlot()
    qb.show()
    sys.exit(app.exec())
