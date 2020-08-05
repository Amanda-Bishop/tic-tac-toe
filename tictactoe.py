from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, re, random
  

class Window(QMainWindow): 
    def __init__(self): 
        super().__init__()
        self.title = 'Tic Tac Toe'
        self.x, self.y, self.w, self.h = 400, 300, 500, 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title) 
        self.setGeometry(self.x, self.y, self.w, self.h)
        self.cursor = QCursor.pos()

        x,y,w,h = 98,18,100,80
        count = 0
        self.btns = QButtonGroup()
        for i in range(9):
            self.btn = QPushButton('', self)
            self.btn.move(x,y)
            self.btn.resize(w,h)
            self.btn.setStyleSheet("background-color: #f5f5f5;")
            self.btns.addButton(self.btn,i)
            x += 103
            w = 98
            count += 1
            if count == 3:
                x,y,w,h = 98,103,100,95
            elif count == 6:
                x,y,w,h = 98,203,100,80

        self.btns.buttonClicked[int].connect(self.onClick)

        self.board = ['','','','','','','','','']
        self.playerTurn = True
        self.msg = QMessageBox()
        self.msg.setStandardButtons(QMessageBox.Close|QMessageBox.Retry)
        self.msg.buttonClicked.connect(self.popupClick)
            
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        
        pen = QPen(Qt.black, 5, Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(200, 20, 200, 280)
        qp.drawLine(300, 20, 300, 280)
        qp.drawLine(100, 100, 400, 100)
        qp.drawLine(100, 200, 400, 200)
        
        qp.end()

    def onClick(self, i):
        if self.board[i] == '' and self.playerTurn:
            self.btns.button(i).setText('X')
            self.btns.button(i).setFont(QFont('Arial', 50))
            self.board[i] = 'X'
            if isWinner(self.board, 'X'):
                self.msg.setText('You won!')
                x = self.msg.exec_()
            elif '' not in self.board:
                self.msg.setText('Tie game')
                x = self.msg.exec_()
            else:
                self.playerTurn = False
                self.changeBoard()
                    

    def changeBoard(self):
        move = computerMove(self.board)
        self.btns.button(move).setText('O')
        self.btns.button(move).setFont(QFont('Arial', 50))
        self.board[move] = 'O'
        if isWinner(self.board, 'O'):
            self.msg.setText('The computer won')
            x = self.msg.exec_()
        elif '' not in self.board:
            self.msg.setText('Tie game')
            x = self.msg.exec_()
        else:
            self.playerTurn = True

    def popupClick(self,i):
        if i.text() == 'Close':
            sys.exit()
        else:
            self.board = ['','','','','','','','','']
            self.playerTurn = True
            for i in range(9):
                self.btns.button(i).setText('')
                   

def isWinner(board, l):
    return ((board[6] == l and board[7] == l and board[8] == l) or
            (board[3] == l and board[4] == l and board[5] == l) or
            (board[0] == l and board[1] == l and board[2] == l) or
            (board[6] == l and board[3] == l and board[0] == l) or
            (board[7] == l and board[4] == l and board[1] == l) or
            (board[8] == l and board[5] == l and board[2] == l) or
            (board[6] == l and board[4] == l and board[2] == l) or
            (board[8] == l and board[4] == l and board[0] == l))

def computerMove(board):
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            if isWinner(board,'O'):
                board[i] = ''
                return i
            board[i] = ''
            
    for i in range(9):
        if board[i] == '':
            board[i] = 'X'
            if isWinner(board,'X'):
                board[i] = ''
                return i
            board[i] = ''

    c = [0,2,6,8]
    random.shuffle(c)
    if board[c[0]] == '':
        return c[0]


    if board[4] == '':
        return 4

    s = [1,3,5,7]
    random.shuffle(s)
    if board[s[0]] == '':
        return s[0]
      
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()

    sys._excepthook = sys.excepthook 
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback) 
        sys.exit(1) 
    sys.excepthook = exception_hook
    
    sys.exit(app.exec())

