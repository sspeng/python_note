#! /usr/bin/python3
# -*- coding: utf8 -*-

import sys
from PyQt5.Qt import *
import cv2

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
        painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
        painter.drawRect(rect)

        pqscreen = QGuiApplication.primaryScreen()
        pixmap2 = pqscreen.grabWindow(self.winId(), self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        pixmap2.save('demo.png')


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.lb = myLabel(self)
        self.initUi()

    def initUi(self):
        self.resize(675, 300)
        self.setWindowTitle("screenShot demo")
        self.lb.setGeometry(140, 30, 511, 241)
        img = cv2.imread('xxx.png')
        height, width, bytePerComponent = img.shape
        bytesPerline = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        Qimg = QImage(img.data, width, height, bytesPerline, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(Qimg)

        self.lb.setPixmap(pixmap)
        self.lb.setCursor(Qt.CrossCursor)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Example()
    window.show()

    sys.exit(app.exec())