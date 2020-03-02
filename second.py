import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLCDNumber, QLabel, QLineEdit, QMainWindow, QInputDialog, QFontDialog
from PyQt5.uic.properties import QtGui


class SP(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('text1.ui', self)
        self.initUI()
 
    def initUI(self):
        self.setGeometry(800, 800, 800, 800)
        self.setWindowTitle('Библиотека')

      # self.settings = QPushButton(self)
       # self.settings.move(420, 720)
        #self.settings.setText('Настройки')
        self.settings.clicked.connect(self.run)

        #self.last = QPushButton(self)
        #self.last.move(60, 690)
        #self.last.setText('Предыдущая')
        ##self.last.clicked.connect(self.run)

        #self.next = QPushButton(self)
        #self.next.move(850, 690)
        #self.next.setText('Следующая')
        ##self.next.clicked.connect(self.run)

        self.Fontn.clicked.connect(self.run2)


        self.show()

    def run(self):
        pass

    def run2(self):
        okBtnPressed, i = QInputDialog.getInt(self, 'Размер шрифта', 'Выберите размер шрифта', 14, 8, 16)
        if okBtnPressed:
        #    self.label.setFont(i, QtGui.QFont.Bold)
            if i == '16':
                self.label.setFont(QtGui.QFont("Courier", 16, QtGui.QFont.Bold))
                self.label.display()
                self.label.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SP()
    ex.show()
    sys.exit(app.exec())  
