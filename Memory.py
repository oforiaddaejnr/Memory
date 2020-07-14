import sys
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer
#import time
import random

CELL_COUNT = 8
CELL_SIZE = 50
GRID_ORIGINX = 175
GRID_ORIGINY = 175

class Memory(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(150, 150, 700, 700)
        self.setWindowTitle('Memory Game')
        self.__timer = QTimer()
        self.__x = -1
        self.__y = -1
        self.__timer.timeout.connect(self.flicker)
        self.empty = ''
        self.emptylist = [[ self.empty for row in range(8)] for col in range(8)]
        self.secondary_list = [[ self.empty for row in range(8)] for col in range(8)]
        self.numlist = random.sample(range(100), 32)
        self.new_numlist = self.numlist + self.numlist #concatenating list to create 64 values with a pair of each number
        random.shuffle(self.new_numlist)
        self.selectedNum = []
        self.takeRow = []
        self.takeColumn = []
        self.pause = False
        self.show()
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                qp.setPen(QPen(Qt.black,0))
                qp.drawRect(col*CELL_SIZE + GRID_ORIGINX, row*CELL_SIZE + GRID_ORIGINY, CELL_SIZE, CELL_SIZE)
        #adding numbers to grid
        counter = 0
        for row in range(len(self.secondary_list)):
            for col in range(len(self.secondary_list[0])):
                self.secondary_list[row][col] = str(self.new_numlist[counter])
                counter += 1
                if self.emptylist[row][col] != '':
                    textPen = QPen(QBrush(Qt.red),3)
                    xcoord = GRID_ORIGINX + col * CELL_SIZE
                    ycoord = GRID_ORIGINY + row * CELL_SIZE
                    qp.setPen(textPen)
                    qp.drawText(QRect(xcoord, ycoord, 50, 50), Qt.AlignCenter,str(self.emptylist[row][col]))
        qp.end()
        print(self.secondary_list)

    def check(self):
        if self.selectedNum[0] != self.selectedNum[1]:
            self.__timer.start(1000)
            self.pause = True
            print(self.emptylist)
            self.selectedNum.clear()
            print("timer started")
        else:
            self.selectedNum.clear()
            self.takeRow.clear()
            self.takeColumn.clear()
            print("timer didn't start")

    def flicker(self):
        self.__timer.stop()
        self.emptylist[self.takeRow[0]][self.takeColumn[0]] = ''
        self.emptylist[self.takeRow[1]][self.takeColumn[1]] = ''
        self.takeRow.clear()
        self.takeColumn.clear()
        self.pause = False
        self.update()

    def mousePressEvent(self,event):
        self.__x = event.x()
        self.__y = event.y()
        print(event.x(), event.y())
        col = (event.x() - GRID_ORIGINX)// CELL_SIZE
        row = (event.y() - GRID_ORIGINY)// CELL_SIZE
        if 0 <= row <8 and 0<= col <8:
            if self.pause == False and self.emptylist[row][col] == '':
                self.emptylist[row][col] = self.secondary_list[row][col]
                if len(self.selectedNum) < 2:
                    self.takeRow.append(row)
                    self.takeColumn.append(col)
                    self.selectedNum.append(str(self.emptylist[row][col]))
                if len(self.selectedNum)== 2:
                    print(self.selectedNum)
                    print(self.takeRow)
                    print(self.takeColumn)
                    self.check()

        print(row, col)
        self.update()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = Memory()
  sys.exit(app.exec_())
