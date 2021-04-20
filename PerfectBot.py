#!/usr/bin/python

import random
import sys
import os
import queue
import Game


class PerfectBot():
    botChoice = None
    choice = None
    def score(self,game):
        if game.playerWon():
            return -10
        elif game.botWon():
            return 10
        else:
            return 0

    def get_choice(self):
        return self.choice


    def minimax(self,game,deapth,isMax,alpha, beta, deapthMax):
        if game.playerWon() or game.botWon() or game.draw() or deapth == deapthMax:
            return self.score(game)
        '''
        mv = game.availableMoves()
        for move in mv:
            # State in which we may be
            possibleGame = game.possibleMove(move)
            scores.append(self.minimax(possibleGame))
            moves.append(move)
        '''

        #if is the bot's turn then we need to maximize the chances of winning
        if(isMax):
            maxim = -sys.maxsize - 1
            for i in range(1,game.get_w() + 1):
                for j in range(1,game.get_w() + 1):
                    if game.Harta[i][j] == 0:
                        game.Harta[i][j] = -1
                        maxim = max(maxim,self.minimax(game, deapth+1, False,alpha,beta,deapthMax))
                        alpha = max(alpha, maxim)
                        game.Harta[i][j] = 0
                        if beta <= alpha:
                            break

            return maxim - deapth

        else:
            minim = sys.maxsize
            for i in range(1,game.get_w() + 1):
                for j in range(1,game.get_w() + 1):
                    if game.Harta[i][j] == 0:
                        game.Harta[i][j] = 1
                        minim = min(minim,self.minimax(game, deapth+1, True,alpha,beta,deapthMax))
                        beta = min(beta,minim)
                        game.Harta[i][j] = 0
                        if beta <= alpha:
                            break
            return minim + deapth







