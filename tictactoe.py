# Import statements
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, re, random
  
# Class for the window 
class Window(QMainWindow):
    # Initialization function
    def __init__(self): 
        super().__init__()
        self.title = 'Tic Tac Toe'
        self.x, self.y, self.w, self.h = 400, 300, 500, 300
        self.board = ['','','','','','','','','']
        self.playerTurn = True
        self.initUI()

    # GUI initialization function
    def initUI(self):
        # Sets the window size and title
        self.setWindowTitle(self.title) 
        self.setGeometry(self.x, self.y, self.w, self.h)

        # Creates button group
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
        self.btns.buttonClicked[int].connect(self.onClick)                      # Connects the buttons to the onClick function

        # Creates the pop up for when the game ends
        self.msg = QMessageBox()
        self.msg.setStandardButtons(QMessageBox.Close|QMessageBox.Retry)
        self.msg.buttonClicked.connect(self.popupClick)
            
        self.show()

    # Function to draw the grid
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

    # Function for when the user clicks on a tile
    def onClick(self, i):
        if self.board[i] == '' and self.playerTurn:
            self.btns.button(i).setText('X')                                    # Places an 'X' on the button
            self.btns.button(i).setFont(QFont('Arial', 50))
            self.board[i] = 'X'                                                 # Marks on the board that the button has been selected
            # Checks if the player has won
            if isWinner(self.board, 'X'):
                self.msg.setText('You won!')
                x = self.msg.exec_()
            # Checks if no one has won
            elif '' not in self.board:
                self.msg.setText('Tie game')
                x = self.msg.exec_()
            # Calls on the computer to change the board
            else:
                self.playerTurn = False
                self.changeBoard()
                    

    # Function to change the board based on the computer's move
    def changeBoard(self):
        move = computerMove(self.board)                                         # Calls on the computerMove function to get the move
        self.btns.button(move).setText('O')                                     # Places an 'O' on the button 
        self.btns.button(move).setFont(QFont('Arial', 50))
        self.board[move] = 'O'                                                  # Marks on the board that the button has been selected
        # Checks if the computer has won
        if isWinner(self.board, 'O'):
            self.msg.setText('The computer won')
            x = self.msg.exec_()
        # Checks if no one has won
        elif '' not in self.board:
            self.msg.setText('Tie game')
            x = self.msg.exec_()
        # Makes it the player's turn 
        else:
            self.playerTurn = True

    # Function for when the popup has been clicked
    def popupClick(self,i):
        # Closes the program if the 'Close' button has been clicked
        if i.text() == 'Close':
            sys.exit()
        # Resets the board if the 'Retry' button has been clicked
        else:
            self.board = ['','','','','','','','','']
            self.playerTurn = True
            for i in range(9):
                self.btns.button(i).setText('')
                   
# Function to check if a player has won given the board and their letter
def isWinner(board, l):
    return ((board[6] == l and board[7] == l and board[8] == l) or              # Checks the board horizontally
            (board[3] == l and board[4] == l and board[5] == l) or              # Checks the board horizontally
            (board[0] == l and board[1] == l and board[2] == l) or              # Checks the board horizontally
            (board[6] == l and board[3] == l and board[0] == l) or              # Checks the board vertically
            (board[7] == l and board[4] == l and board[1] == l) or              # Checks the board vertically
            (board[8] == l and board[5] == l and board[2] == l) or              # Checks the board vertically
            (board[6] == l and board[4] == l and board[2] == l) or              # Checks the board diagonally
            (board[8] == l and board[4] == l and board[0] == l))                # Checks the board diagonally

# Function to select the computer's move
def computerMove(board):
    # Checks to see if the computer can win in the next move and if so picks that move
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            if isWinner(board,'O'):
                board[i] = ''
                return i
            board[i] = ''

    # Checks to see if the user can win in the next move and if so picks the move to block that
    for i in range(9):
        if board[i] == '':
            board[i] = 'X'
            if isWinner(board,'X'):
                board[i] = ''
                return i
            board[i] = ''

    # Randomly selects a corner and picks that move if it's empty
    c = [0,2,6,8]
    random.shuffle(c)
    if board[c[0]] == '':
        return c[0]

    # Picks the center if it's empty
    if board[4] == '':
        return 4

    # Randomly selects a side and picks that move if it's empty
    s = [1,3,5,7]
    random.shuffle(s)
    if board[s[0]] == '':
        return s[0]

# Runs the code     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())

