#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
PyQt5 tutorial
 
In this example we draw 6 lines using
different pen styles.
 
author: py40.com
last edited: 2017年3月
"""
from __future__ import print_function

import pickle
import sys


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QWidget

import greenlet
from game import Board, Game
from mcts_alphaZero import MCTSPlayer
from policy_value_net_numpy import PolicyValueNetNumpy
from mcts_pure import MCTSPlayer as MCTS_Pure

weight = 19
height = 19
n = 5
model_file = 'current_policy2.model'
humanFirst = False



class Human(object):
    """
    human player
    """

    def __init__(self, gui):
        self.player = None
        self.gui = gui

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        out = {"out": -1}
        ex.robootMove(board.last_move, out)
        g1.switch()
        try:
            move = out["out"]
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.weight = weight
        self.height = height
        self.everyLine = 40
        self.pos_x = 0
        self.pos_y = 0
        self.canPlay = False
        if(humanFirst):
            self.player = 1
            self.playerR = 2
        else:
            self.player = 2
            self.playerR = 1
        self.winer = -2
        self.graphic = [[0 for i in range(self.weight+1)]
                        for i in range(self.height+1)]
        self.initUI()
        g2.switch()

    def initUI(self):
        self.setGeometry(300, 300, (self.weight+2) *
                         self.everyLine + 300, (self.height+2)*self.everyLine)
        self.setWindowTitle('五子棋')
        global ex
        ex = self
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QPen(QColor(130, 130, 130)))
        qp.setBrush(QBrush(QColor(130, 130, 130), Qt.SolidPattern))
        qp.drawRect(0, 0, (self.weight+2) *
                    self.everyLine, (self.height+2)*self.everyLine)
        self.drawLines(qp)
        self.drawPoints(qp)
        self.drawRect(qp)
        self.drawText(qp)
        qp.end()

    def drawText(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        if(self.canPlay):
            txt = "你的回合"
        else:
            if(self.winer == -2):
                txt = "电脑的回合"
            elif(self.winer == -1):
                txt = "游戏结束,平局"
            elif(self.winer == 1):
                txt = "游戏结束,恭喜您获胜"
            else:
                txt = "游戏结束,电脑获胜"
        qp.drawText((self.weight+2) * self.everyLine, self.everyLine, txt)

    def drawLines(self, qp):
        pen = QPen(Qt.black, 4, Qt.SolidLine)

        qp.setPen(pen)
        # qp.drawLine(20, 40, 250, 40)
        for num in range(1, self.weight+1):
            qp.drawLine(num*self.everyLine, self.everyLine, num *
                        self.everyLine, self.weight*self.everyLine)
        for num in range(1, self.height+1):
            qp.drawLine(self.everyLine, num*self.everyLine,
                        self.height*self.everyLine, num*self.everyLine)

    def drawPoints(self, qp):
        
        for i in range(1, self.height+1):
            for j in range(1, self.weight+1):
                if(self.graphic[i][j] == 1):
                    qp.setPen(QPen(Qt.black))
                    qp.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                    qp.drawEllipse(
                        (j-0.25)*self.everyLine,
                        (i-0.25)*self.everyLine,
                        self.everyLine/2,
                        self.everyLine/2
                    )
                elif(self.graphic[i][j] == 2):
                    qp.setPen(QPen(Qt.white))
                    qp.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                    qp.drawEllipse(
                        (j-0.25)*self.everyLine,
                        (i-0.25)*self.everyLine,
                        self.everyLine/2,
                        self.everyLine/2
                    )

    def drawRect(self, qp):
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        x, y, lenth = self.pos_x, self.pos_y, self.everyLine
        if(1 <= x <= self.weight and 1 <= y <= self.height):
            qp.drawLine((x-0.5)*lenth, (y-0.5)*lenth,
                        (x-0.5)*lenth, (y+0.5)*lenth)
            qp.drawLine((x-0.5)*lenth, (y-0.5)*lenth,
                        (x+0.5)*lenth, (y-0.5)*lenth)
            qp.drawLine((x+0.5)*lenth, (y+0.5)*lenth,
                        (x-0.5)*lenth, (y+0.5)*lenth)
            qp.drawLine((x+0.5)*lenth, (y+0.5)*lenth,
                        (x+0.5)*lenth, (y-0.5)*lenth)

    def mouseMoveEvent(self, event):
        x = round(event.pos().x()+0.5*self.everyLine)//self.everyLine
        y = round(event.pos().y()+0.5*self.everyLine)//self.everyLine
        if(
            (x != self.pos_x or y != self.pos_y)
            and self.canPlay
            and self.graphic[y][x] == 0
        ):
            self.pos_x, self.pos_y = x, y
            self.repaint()

    def mousePressEvent(self,  event):
        x = round(event.pos().x()+0.5*self.everyLine)//self.everyLine
        y = round(event.pos().y()+0.5*self.everyLine)//self.everyLine
        if(
            (x == self.pos_x and y == self.pos_y)
            and self.canPlay
            and self.graphic[y][x] == 0
        ):
            self.pos_x, self.pos_y = 0, 0
            self.graphic[y][x] = self.player
            self.canPlay = False
            self.out["out"] = (self.height - y) * self.weight + x - 1
            self.repaint()
            g2.switch()
        else:
            self.mouseMoveEvent(event)

    def robootMove(self, move, cb=None):
        if(move != -1):
            h = move // self.weight
            w = move % self.weight
            loaction = [h, w]
            x = loaction[1] + 1
            y = self.height - loaction[0]
            if(self.graphic[y][x] == 0):
                self.graphic[y][x] = self.playerR
        if(cb):
            self.canPlay = True
        self.out = cb
        self.repaint()

    def endTheGame(self, win, move):
        self.canPlay = False
        self.winer = win
        self.robootMove(move=move)


ex = None


def gui():
    global app
    app = QApplication(sys.argv)
    ex = Example()


def ai():
    try:
        board = Board(width=weight, height=height, n_in_row=n)
        game = Game(board)

        # ############### human VS AI ###################
        # load the trained policy_value_net in either Theano/Lasagne, PyTorch or TensorFlow

        # best_policy = PolicyValueNet(weight, height, model_file = model_file)
        # mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

        # load the provided model (trained in Theano/Lasagne) into a MCTS player written in pure numpy
        
        try:
            policy_param = pickle.load(open(model_file, 'rb'))
        except:
            policy_param = pickle.load(open(model_file, 'rb'),
                                       encoding='bytes')  # To support python3
        best_policy = PolicyValueNetNumpy(weight, height, policy_param)
        mcts_player = MCTSPlayer(best_policy.policy_value_fn,
                                 c_puct=5,
                                 n_playout=400)  # set larger n_playout for better performance

        # uncomment the following line to play with pure MCTS (it's much weaker even with a larger n_playout)
        # mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

        # human player, input your move in the format: 2,3
        human = Human(gui=ex)

        # set start_player=0 for human first
        if(humanFirst):
            start_player = 0
        else:
            start_player = 1
        ex.endTheGame(win=game.start_play(human, mcts_player,
                                          start_player=start_player, is_shown=0),
                      move=board.last_move)
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    g1 = greenlet.greenlet(gui)
    g2 = greenlet.greenlet(ai)
    g1.switch()
    sys.exit(app.exec_())
