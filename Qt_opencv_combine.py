#! /usr/bin/python3
# -*- coding: utf8 -*-

from PyQt5.Qt import *

class myLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self, event:QMouseEvent):
        self.flag = True
        self.x0 = event.x()
        self.y1 = event.y()

    def mouseReleaseEvent(self, event:QMouseEvent):
        self.flag = False

    def mouseMoveEvent(self, event:QMouseEvent):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event:QPaintEvent):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(Qt.red, 4, Qt.SolidLine)
        painter.drawRect(rect)

        pqscreen = QGuiApplication.primaryScreen()
        pixmap2 = pqscreen.grabWindow(self.winId(), self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        pixmap2.save('demo.png')


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        pass