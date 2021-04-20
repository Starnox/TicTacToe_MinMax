import random
import sys
import os
import queue
import PerfectBot
from queue import Queue

from tkinter import *


class Game:
    __w = 0
    Harta = []
    botTurn = False

    # variable for holding whose turn is( 1 - for player, 0 - for the bot)
    # the player will always start first TODO implement a function that lets the computer start first
    __currentTurn = 1

    def get_Harta(self):
        return self.Harta
    def set_Harta(self, newHarta):
        self.Harta = newHarta

    def get_w(self):
        return self.__w

    def __init__(self, harta):
        self.__w = 3
        self.Harta = harta


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

    def Computer(self):
        bestCol = -1
        bestRow = -1
        bestVal = -1000
        bot = PerfectBot.PerfectBot()
        for i in range(1, self.__w + 1):
            for j in range(1, self.__w + 1):
                if self.Harta[i][j] == 0:
                    self.Harta[i][j] = -1
                    moveVal = bot.minimax(self, 0, False,-1000,1000)
                    print(moveVal,end=" ")

                    self.Harta[i][j] = 0
                    if moveVal > bestVal:
                        bestVal = moveVal
                        bestRow = i
                        bestCol = j
        self.Harta[bestRow][bestCol] =-1
        print()

    def possibleMove(self, move):
        possibleMap = self.Harta
        if(self.whoseTurn() == 0):
            possibleMap[self.toRow(move)][self.toCol(move)] = 1
        else:
            possibleMap[self.toRow(move)][self.toCol(move)] = -1
        return Game(possibleMap)


    def play(self):
        while not(self.playerWon() or self.botWon() or self.draw()):
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
