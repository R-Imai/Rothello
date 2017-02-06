#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import codecs
import re

import numpy as np

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

class othello:
	def __init__(self):
		self.board = [[0 for i in range(8)] for j in range(8)]
		self.board[3][3] = 1
		self.board[4][4] = 1
		self.board[3][4] = -1
		self.board[4][3] = -1
		#self.board = [[-1 * (((i+j)%2-1)*2+1) for i in range(8)] for j in range(7)]
		#self.board.append([0 for i in range(8)])
		self.putable = [[0 for i in range(8)] for j in range(8)]
		self.update_putable()
		self.next = -1
		self.cat()
		self.count()
		self.is_end = False

	def cat(self):
		stone = {-1:u"◎", 0:u"　", 1:u"●"}
		self.board_str = " a  b  c  d  e  f  g  h\n"
		print(" a  b  c  d  e  f  g  h")
		for i, elem in enumerate(self.board):
			self.board_str += str(i + 1) + str(elem).replace(", ", "|").replace("-1", stone[-1]).replace("0", stone[0]).replace("1", stone[1]).replace("[", "").replace("]", "") + "|\n"
			print(str(i + 1) + str(elem).replace(", ", "|").replace("-1", stone[-1]).replace("0", stone[0]).replace("1", stone[1]).replace("[", "").replace("]", "") + "|")
	
	def cat_ab(self):
		stone = {-1:u"◎", 0:u"　", 1:u"●"}
		print(" a  b  c  d  e  f  g  h")
		for i, elem in enumerate(self.putable):
			print(str(i + 1) + str(elem).replace(", ", "|").replace("-1", stone[-1]).replace("0", stone[0]).replace("1", stone[1]).replace("[", "").replace("]", ""))
	
	def reverse(self, p1, p2, d):
		x = p1[0] + d[0]
		y = p1[1] + d[1]
		while x != p2[0] or y != p2[1]:
			self.board[x][y] *= -1
			x += d[0]
			y += d[1]

	def is_edge(self, x, y):
		is_check = False
		if x >= 8 or y >= 8:
			is_check = True
		if x < 0 or y < 0:
			is_check = True
		return is_check

	def check(self, x, y):
		direct = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		color = self.board[x][y]
		for d in direct:
			is_check = True
			xx = x + d[0]
			yy = y + d[1]
			if self.is_edge(xx,yy):
				is_check = False
			while is_check:
				if self.board[xx][yy] == 0:
					is_check = False
				elif self.board[xx][yy] == color:
					self.reverse([x, y], [xx,yy], d)
					is_check = False
				xx += d[0]
				yy += d[1]
				if self.is_edge(xx,yy):
					is_check = False

	def is_al(self, al):
		checker = re.compile(r'^[a-j]+$')
		return checker.match(al) is not None
	
	def is_around(self, x, y):
		for i in range(-1, 2):
			for j in range(-1, 2):
				if x + i >= 0 and y + j >= 0 and x + i < 8 and y + j < 8:
					if self.board[x + i][y + j] != 0:
						return True
		return False

	def update_putable(self):
		for j in range(8):
			for i in range(8):
				if self.board[i][j] == 0:
					if self.is_around(i, j):
						self.putable[i][j] = 1
					else :
						self.putable[i][j] = 0
				else:
					self.putable[i][j] = 0
	def is_set(self, x, y, color):
		re = False
		if self.putable[x][y] == 1:
			direct = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
			for d in direct:
				is_check = True
				xx = x + d[0]
				yy = y + d[1]
				if self.is_edge(xx,yy):
					is_check = False
				fg = False
				while is_check:
					if self.board[xx][yy] == 0:
						is_check = False
					elif self.board[xx][yy] == -1*color:
						fg = True
					elif self.board[xx][yy] == color:
						if fg:
							re = True
						is_check = False
					xx += d[0]
					yy += d[1]
					if self.is_edge(xx,yy):
						is_check = False
		return re

	def next_p(self):
		self.next *= -1
		is_change = True
		end_fg = False 
		for j in range(8):
			for i in range(8):
				if self.is_set(i, j, self.next):
					is_change = False
		if is_change:
			self.next *= -1
			

	def count(self):
		self.brack_cnt = 0
		self.white_cnt = 0
		self.brank_cnt = 0
		for elem in self.board:
			self.white_cnt += elem.count(1)
			self.brack_cnt += elem.count(-1)
			self.brank_cnt += elem.count(0)

	def is_finish(self):
		self.count()
		re = False
		if self.brack_cnt == 0 or self.white_cnt == 0:
			re = True
		elif self.brank_cnt == 0:
			re = True
		return re

	def set(self, x, y, color):
		if self.is_al(y) and x.isdigit():
			pass
		elif self.is_al(x) and y.isdigit():
			z = y
			y = x
			x = z
		else :
			return -1
		if 0 >= int(x) or int(x) > 8:
			return -1
		x = int(x) - 1
		y = ord(y) - 97
		if self.is_set(x,y,color):
			self.board[x][y] = int(color)
			self.check(x, y)
			self.update_putable()
		else:
			return 1
		self.next_p()
		if self.is_finish():
			return 10
		return 0

def board_str2arr(board_str):
	board_str = board_str.replace(" a  b  c  d  e  f  g  h","").replace("|", "").replace("\n", "")
	for i in range(1, 9):
		board_str = board_str.replace(str(i), "")
	board_str = board_str.replace("◎", "0")
	board_str = board_str.replace("　", "1")
	board_str = board_str.replace("●", "2")
	arr = np.array(map(int, list(board_str))) - 1
	arr = arr.reshape(8,8)
	return arr

	

def main():
	model = othello()
	model.cat()
	model.cat_ab()
	usr = [1, -1]
	colors = ["white","brack"]
	for i in range(6):
		re = 1
		while re != 0:
			print(colors[int(i)%2] + "'s turn")
			s = raw_input().split(" ")
			re = model.set(s[0], s[1],usr[int(i)%2])
			print(re)
			if re == -1:
				print("error")
			if re == 1:
				print("put error")	
		model.cat()
		model.cat_ab()
	
if __name__ == "__main__":
	main()
