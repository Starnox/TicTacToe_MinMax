import random
import sys
import os
import queue
import PerfectBot
from queue import Queue


import pygame
from pygame.locals import *

class Game:
    #Constants
    NUMBER_OF_BLOCKS = 3
    NUMBER_OF_STEPS = 5
    WIDTH = 500
    HEIGHT = 500

    Harta = []
    botTurn = False

    # variable for holding whose turn is( 1 - for player, 0 - for the bot)
    # the player will always start first implement a function that lets the computer start first - DONE

    # Constructors

    def __init__(self, harta, size):
        self.__w = size
        self.Harta = harta
        self.__currentTurn  = 1

    def __init__(self):
        self.__w =  self.NUMBER_OF_BLOCKS
        self.Harta = [[0 for x in range(0, self.__w + 1)] for y in range(0 + self.__w + 1)]
        self.__currentTurn = 1

        #Pygame intialisation
        pygame.init()
        pygame.display.set_caption("TicTacToe")
        self.__screen =  pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.__screen.fill((250,250,250))

    # Getters and Setters
    def get_Harta(self):
        return self.Harta
    def set_Harta(self, newHarta):
        self.Harta = newHarta

    def get_w(self):
        return self.__w


    #Prints the map to the console
    def printMap(self):
        print(self.__w + 1)
        for i in range(1, self.__w + 1):
            for j in range(1, self.__w + 1):
                if (self.Harta[i][j] == -1):
                    print('O', end="")
                elif (self.Harta[i][j] == 1):
                    print('X', end="")
                else:
                    print("_", end="")
                if(j <= self.__w - 1):
                    print("|", end="")
            print()
        return;

    def availableMoves(self):
        moves = []
        for i in range(1, self.__w * self.__w + 1):
            row = self.toRow(i)
            col = self.toCol(i)
            if self.Harta[row][col] == 0:
                moves.append(i)
        return moves

    def toCol(self,x):
        if (x % self.__w != 0):
            return x % self.__w
        else:
            return self.__w

    def toRow(self,x):
        if(x % self.__w != 0):
            return x // self.__w + 1
        else:
            return x // self.__w

    def AskUser(self):
        print("Select a value beetween [0,%d]" % (self.__w * self.__w))
        response = int(sys.stdin.readline())
        if(response >= 1) and (response <= self.__w * self.__w) and self.Harta[self.toRow(response)][self.toCol(response)] == 0:
            self.Harta[self.toRow(response)][self.toCol(response)] = 1
        else:
            print("Please select a valid choice")
            self.AskUser()

    def Computer(self,board):
        bestCol = -1
        bestRow = -1
        bestVal = -1000
        bot = PerfectBot.PerfectBot()
        for i in range(1, self.__w + 1):
            for j in range(1, self.__w + 1):
                if self.Harta[i][j] == 0:
                    self.Harta[i][j] = -1
                    moveVal = bot.minimax(self, 0, False, -1000, 1000, self.NUMBER_OF_STEPS)
                    print(moveVal,end=" ")

                    self.Harta[i][j] = 0
                    if moveVal > bestVal:
                        bestVal = moveVal
                        bestRow = i
                        bestCol = j
        self.__currentTurn = 1
        self.Harta[bestRow][bestCol] =-1
       # self.drawMove(board,bestRow,bestCol,-1)
        print()

    def possibleMove(self, move):
        possibleMap = self.Harta
        if(self.whoseTurn() == 0):
            possibleMap[self.toRow(move)][self.toCol(move)] = 1
        else:
            possibleMap[self.toRow(move)][self.toCol(move)] = -1
        return Game(possibleMap)

    def InitBoard(self):
        white = (250, 250, 250)
        black = (0, 0, 0)

        background = pygame.Surface((310,310))
        background = background.convert()

        background.fill((250, 250, 250))
        pygame.draw.line(background, black, (0, 0), (0, 300), 2)
        pygame.draw.line(background, black, (0, 0), (300, 0), 2)
        pygame.draw.line(background, black, (300, 0), (300, 300), 2)
        pygame.draw.line(background, black, (300, 300), (0, 300), 2)
        pygame.draw.line(background, (0, 0, 0), (100, 0), (100, 300), 2)
        pygame.draw.line(background, (0, 0, 0), (200, 0), (200, 300), 2)

        # horizontal lines...
        pygame.draw.line(background, (0, 0, 0), (0, 100), (300, 100), 2)
        pygame.draw.line(background, (0, 0, 0), (0, 200), (300, 200), 2)

        return  background

    def GameOver(self):
        if self.playerWon():
            self.__currentTurn = 1
            return True
        elif self.botWon():
            self.__currentTurn = 0
            return True
        elif self.draw():
            self.__currentTurn = (self.__currentTurn + 1) % 2
            return True
        else: return False

    def boardPos(self, mouseX, mouseY):
        # given a set of coordinates from the mouse, determine which board space
        # (row, column) the user clicked in.
        # ---------------------------------------------------------------
        # mouseX : the X coordinate the user clicked
        # mouseY : the Y coordinate the user clicked

        # determine the row the user clicked
        if (mouseY < 100):
            row = 1
        elif (mouseY < 200):
            row = 2
        else:
            row = 3

        # determine the column the user clicked
        if (mouseX < 100):
            col = 1
        elif (mouseX < 200):
            col = 2
        else:
            col = 3

        # return the tuple containg the row & column
        return (row, col)

    def mouseClick(self,board):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        (row, col) = self.boardPos(mouseX,mouseY)
        print(row,col)
        if self.Harta[row][col] == 0:
            self.Harta[row][col] = 1
            #self.drawMove(board,row,col,1)
            self.__currentTurn = 0
        else:
            return


    def drawMove(self,board,boardRow,boardCol,Piece):
        centerX = ((boardCol) * 100) - 50
        centerY = ((boardRow) * 100) - 50

        # draw the appropriate piece
        if (Piece == -1):
            pygame.draw.circle(board, (0, 0, 0), (centerX, centerY), 44, 2)
        else:
            pygame.draw.line(board, (0, 0, 0), (centerX - 22, centerY - 22),
                             (centerX + 22, centerY + 22), 2)
            pygame.draw.line(board, (0, 0, 0), (centerX + 22, centerY - 22),
                             (centerX - 22, centerY + 22), 2)

    def RefreshBoard(self,main,board):

        for i in range(1, self.__w + 1):
            for j in range(1, self.__w + 1):
                if self.Harta[i][j] == 1:
                    self.drawMove(board, i, j, 1)
                elif self.Harta[i][j] == -1:
                    self.drawMove(board, i, j, -1)

        main.blit(board, (0, 0))
        pygame.display.flip()

    def play(self):

        white = (250, 250, 250)
        black = (0, 0, 0)
        # draw the grid lines
        # vertical lines...
        gameOver = False
        restartGame = False
        clock = pygame.time.Clock()

        board = self.InitBoard()

        while True:
            gameOver = self.GameOver()
            if gameOver and restartGame:
                restartGame = False
                gameOver = False
                self.resetGame()
                board = self.InitBoard()
                self.RefreshBoard(self.__screen, board)
                continue

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                    if self.__currentTurn == 1:
                        self.mouseClick(board)
                        self.GameOver()
                        self.RefreshBoard(self.__screen,board)
                        continue;
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        restartGame = True


            if self.__currentTurn == 0 and not gameOver:
                self.Computer(board)

            self.RefreshBoard(self.__screen,board)

            pygame.display.flip()
            clock.tick(120)

        print("Hello")
        '''
        while not self.playerWon() or self.botWon() or self.draw() :
            self.AskUser()
            self.__currentTurn = 1
            if self.playerWon() or self.botWon() or self.draw():
                break

            self.__currentTurn = 0
            self.Computer()
            if self.playerWon() or self.botWon() or self.draw():
                break

            moves = self.availableMoves()
            for i in moves:
                print(i, end=" ")
            print()

            self.printMap()
        self.printMap()
        '''

    def whoseTurn(self):
        ct = 0
        for i in range(1 , self.__w + 1):
            for j in range(1, self.__w + 1):
                if(self.Harta[i][j] != 0):
                    ct+=1

        # if the board is clear then is the player's turn - 1
        if ct == 0:
            return 1
        elif ct % 2 == 0:
            return 1
        else:
            return 0

    def resetGame(self):
        for i in range(1, self.__w + 1):
            for j in range(1, self.__w + 1):
                self.Harta[i][j] = 0


    def playerWon(self):

        ok = True
        # checks horizontally
        for i in range (1, self.__w +1):
            first = self.Harta[i][1]
            ok = True
            for j in range(1 , self.__w + 1):
                if(first == 0 ) or first != self.Harta[i][j]:
                    ok = False
            if(ok == True):
                if (first == 1):
                    return True


        # checks vertically
        ok = True
        for j in range (1, self.__w +1):
            first = self.Harta[1][j]
            ok = True
            for i in range(1 , self.__w + 1):
                if(first == 0 ) or first != self.Harta[i][j]:
                    ok = False
            if (ok == True):
                if (first == 1):
                    return True

        # checks diagonally
            # checks first diagonal
        first = self.Harta[1][1]
        ok = True
        for i in range (1, self.__w + 1):
            if (first == 0) or first != self.Harta[i][i]:
                ok = False
        if(ok == True):
            if (first == 1):
                return True

            # checks second diagonal
        first = self.Harta[1][self.__w]
        ok = True
        for i in range (1, self.__w + 1):
            if (first == 0) or first != self.Harta[i][self.__w - i + 1]:
                ok = False
        if(ok == True):
            if (first == 1):
                return True

        return False


    def botWon(self):

        # we're assuming we have a draw

        ok = True
        # checks horizontally
        for i in range (1, self.__w +1):
            first = self.Harta[i][1]
            ok = True
            for j in range(1 , self.__w + 1):
                if(first == 0 ) or first != self.Harta[i][j]:
                    ok = False
            if(ok == True):
                if (first == -1):
                    return True

        # checks vertically
        ok = True
        for j in range (1, self.__w +1):
            first = self.Harta[1][j]
            ok = True
            for i in range(1 , self.__w + 1):
                if(first == 0 ) or first != self.Harta[i][j]:
                    ok = False
            if (ok == True):
                if (first == -1):

                    return True

        # checks diagonally
            # checks first diagonal
        first = self.Harta[1][1]
        ok = True
        for i in range (1, self.__w + 1):
            if (first == 0) or first != self.Harta[i][i]:
                ok = False
        if (ok == True):
            if (first == -1):
                return True

            # checks second diagonal
        first = self.Harta[1][self.__w]
        ok = True
        for i in range (1, self.__w + 1):
            if (first == 0) or first != self.Harta[i][self.__w - i + 1]:
                ok = False
        if (ok == True):
            if (first == -1):
                return True

        return False


    def draw(self):
        # we're assuming we have a draw
        draw = True

        # if  the board is full then it's a draw
        for i in range(1, self.__w + 1):
            for j in range(1, self.__w + 1):
                if (self.Harta[i][j] == 0):
                    # if a space is cleared then we don't have a draw
                    draw = False

        if (draw):
            return True
