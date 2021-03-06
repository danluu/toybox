from __future__ import print_function
import numpy as np
import random

class Game(object):
    def __init__(self, width, height, num_mines):
        self.board = self.generate_board(width, height, num_mines)
        # What spaces the player knows about
        self.known = self.generate_board(width, height, 0)
        self.num_moves = 0

    @staticmethod
    def generate_board(width, height, mine_prob):
        board = [[0 for _ in range(width)] for _ in range(height)]
        for rindex,row in enumerate(board):
            for cindex,col in enumerate(row):
                if random.random() < mine_prob:
                    board[rindex][cindex] = 1
        return board

    def move(self, row, col):
        self.known[row][col] = 1
        self.num_moves += 1
        return self.board[row][col]

    def print_board(self):
        for rindex,row in enumerate(self.board):
            for cindex,col in enumerate(row):
                if self.known[rindex][cindex]:
                    print(self.get_output_at_location(rindex, cindex), end='')
                else:
                    print('?', end='')
            print('')

    def get_output_at_location(self, row, col):
        if self.board[row][col]:
            return "X" # Bomb
        else:
            return str(self.get_num_surrounding_bombs(row, col))

    def get_num_surrounding_bombs(self, row, col):
        # There is probabaly a much nicer way to do this
        sum = 0
        left = col > 0
        right = col < len(self.board[0])-1
        top = row > 0
        bottom = row < len(self.board)-1

        if top:
            sum += self.board[row-1][col]
            if right:
                sum += self.board[row-1][col+1]
            if left:
                sum += self.board[row-1][col-1]
        if bottom:
            sum += self.board[row+1][col]
            if right:
                sum += self.board[row+1][col+1]
            if left:
                sum += self.board[row+1][col-1]
        if left:
            sum += self.board[row][col-1]
        if right:
            sum += self.board[row][col+1]

        return sum

    def get_ml_output_at_location(self, row, col):
        if self.known[row][col]:
            if self.board[row][col]:
                return [0]*9
            else:
                num = self.get_num_surrounding_bombs(row, col)
                return [0]*(num+1) + [1] + [0]*(7-num)
        else:
            return [1] + [0]*8

    def output_ml(self):
        output = []
        for rindex,row in enumerate(self.board):
            for cindex,col in enumerate(row):
                    output += self.get_ml_output_at_location(rindex, cindex)
        return output

    def get_reward(self):
        return float(np.sum(self.known) * np.sum(self.known)/self.num_moves)

    def game_over(self):
        for rindex,row in enumerate(self.board):
            for cindex,col in enumerate(row):
                if self.known[rindex][cindex] and self.board[rindex][cindex]:
                    return True
        return False
