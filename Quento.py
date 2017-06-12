""" QUNETO GAME """


import tkinter as tk
from random import sample, choices


BOARDS = []
MARGIN = 20
SIDE = 100
WIDTH = HEIGHT = 340



class QuentoError(Exception):
    """
    An applicaion specific error
    """
    pass

class QuentoCell(object):
    def __init__(self, entry, position):
        self.entry = entry
        self.position = position
        
        self.selected = False
        self.color = 'black'    # black or white

    def __str__(self):
        return str(self.entry)

    def __add__(self, other):
        "i redefine +"
        x1, y1 = self.position
        x2, y2 = other.position
        if abs(x1-x2) > 1 or abs(y1-y2) > 1:
            return False
        return True
 
    def __eq__(self, other):
        return self.position == other.position
    

        

class QuentoBoard(object):
    """
    Quento Board representation
    """
    def __init__(self):
        self.deal_numbers = self.__deal_numbers()
        self.board = self.__create_board()
        self.answers = self.__create_answers()

    def __create_board(self):
        board = [[0, '+', 0],
                 ['-', 0, '-'],
                 [0, '+', 0]]
        
        c = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    entry = self.deal_numbers[c]
                    c += 1
                else:
                    entry = board[i][j]
                board[i][j] = QuentoCell(entry, (i, j))
        
        return board
    
    def __deal_numbers(self):
        "return 5 randoms integers  between 1 and 9"
        return sample(range(1, 10), 5)


    def __create_answers(self):
        "choice 3 item form answers"
        a, b, c, d, e = self.deal_numbers
        answers = [c+a, c-a, c+b, c-b, c+d, c-d, c+3, c-e, a+b, d+e]    # genearte answers
        answers = [abs(i) for i in answers if i != 0]                   # remove negative
        answers = list(set(answers))                                    # remove duplicate
        return choices(answers, k=3)
    

    def __contains__(self, key):
        try:
            key = int(key)
        except:
            key = key
        for row in self.board:
            for col in row:
                if key == col.entry:
                    return True
        return False

    def __str__(self):
        string = ''
        for row in game.board:
            for col in row:
                string += str(col) + '\t'
            string += '\n'
        return string
        


class QuentoGame():
    """
    A Quento game, ...
    """
    def __init__(self):
        self.start()
        
    def start(self):
        "start"
        self.start_puzzle = QuentoBoard()
        self.board = self.start_puzzle.board
        self.answers = self.start_puzzle.answers

        self.chain = ""
        self.count = 0
        self.actions = []
        self.current = None
        self.last = None
        
        self.answer = self.answers[self.count]

    def valid_steep(self):        
        if not self.current in self.start_puzzle:
            return False
        
        if len(self.actions)%2 == 0 and not self.current.isdigit():
            return False
        
        if len(self.actions)%2 == 1 and self.current.isdigit():
            return False
        
        if len(self.actions) != 0:
            if not (self.last + self.current):
                return False
            
        # if is valid
        self.last = self.current
        self.actions.append(str(self.current))
        self.chain += str(self.current)
        return True

    def check_win(self):
        if len(self.actions) != 3:
            return
        
        if self.calcul_chain() != self.answer:
            print(self.chain, " # ", self.answer, ":(")
            self.actions = []
            self.chain = ''
            return False
        
        print(self.chain , " = ", self.answer, ":)")
        self.count += 1

        if self.count > 2:
            self.answer = None
            print("you win :)")
            return True
        
        self.answer = self.answers[self.count]
        print('the answer changed to...', self.answer)
        self.actions = []
        self.chain = ''

    def calcul_chain(self):
        if len(self.chain)%2 == 0:
            self.chain = self.chain[:-1]
        return eval(self.chain)
        

    
class QuentoUI(tk.Frame):
    """
    the tkinter UI,responsible for drawing board
    """
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        tk.Frame.__init__(self, parent)

        self.row, self.col = 0, 0 

        self.__initUI()
        self.pack()

    def __initUI(self):
        self.parent.title("QUENTO")
        self.pack(fill='both', expand=1)
        self.canvas = tk.Canvas(self,
                                width=WIDTH,
                                height=HEIGHT)
        self.canvas.pack()
        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)

    def __draw_grid(self):
        "Draws grid divided with lines 3x3 squares"
        for i in range(3):
            for j in range(3):                
                x0 = MARGIN + j * SIDE
                y0 = MARGIN + i * SIDE
                x1 = MARGIN + (j + 1) * SIDE
                y1 = MARGIN + (i + 1) * SIDE
                fill= "black" if (i+j) % 2 == 0 else 'white'
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, tag=(i,j))


    def __draw_puzzle(self):
        for i in range(3):
            for j in range(3):
                x = MARGIN + j * SIDE + SIDE/ 2
                y = MARGIN + i * SIDE + SIDE/ 2
                text = self.game.board[i][j].entry
                self.canvas.create_text(x, y, text=text, fill='pink')

    def __cell_clicked(self, event):
        x, y = event.x, event.y
        # get row and col numbers from x,y coordinates
        row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE
        print(x, y)
        # if cell was selected already - deselect it

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )



if __name__ == '__main__':
    game = QuentoGame()
    game.start()

    while True:
        game.current = input("Entre your cell: ")
        game.valid_steep()
        game.check_win()
        if game.answer == None:
            break

    root = tk.Tk()
    QuentoUI(root, game)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()
##    game = QuentoGame()
##    while True:
##        print('\t', game.answer)
##        print('-----')
##        print(game.start_puzzle)
##        game.current = input("Entre your cell: ")
##        game.valid_steep()
##        game.check_win()
##        print()
##        if game.answer == None:
##            break
