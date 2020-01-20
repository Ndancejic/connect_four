from copy import deepcopy

MIN = -10000
MAX = 10000
MAX_DEPTH = 5
DEFAULT = 0
P1 = 'X'
P2 = 'O'
alpha = 0.1

class AI_player:
	def __init__(self, Player, Other):
		self.name = "Michael"
		self.player = Player
		self.other = Other

	def make_move(self, b, depth, Player):
		if depth == 0 or b.check_win(Player):
			value = b.heuristic(Player)
			return value, DEFAULT
		move = DEFAULT
		if Player == self.player:
			value = MIN
			for i in range(b.length):
				b1 = deepcopy(b)
				if b1.is_valid(i):
					b1.play(i, Player)
					turn = self.make_move(b1, depth - 1, self.other)
					if turn[0] > value:
						move = i
					value = max(value, turn[0])
			loops = 0
			while not b1.is_valid(move) and loops < b.length:
				move = (move + 1) % b.length
				loops = loops + 1
			return value, move
		else:
			value = MAX
			for i in range(b.length):
				b1 = deepcopy(b)
				if b1.is_valid(i):
					b1.play(i, Player)
					turn = self.make_move(b1, depth - 1, self.player)
					if turn[0] < value:
						move = i
					value = min(value, turn[0])
			loops = 0
			while not b1.is_valid(move) and loops < b.length:
				move = (move + 1) % b.length
				loops = loops + 1
			return value, move

class board():
	def __init__(self, length = 6, width = 6, win_cond = 4):
		self.length = length
		self.width = width
		self.win_cond = win_cond
		self.position = [[' ' for i in range(length)] for j in range (width)]

	def draw_board(self):
		for i in range(self.length):
			print('|', end="")
			for j in range(self.width):
				print(self.position[i][j] + '|', end="")
			print('\n')

	def is_full(self):
		for i in range(self.length):
			for j in range(self.width):
				if self.position[i][j] == ' ':
					return False
		return True

	def checkwin(self, depth, i, j, player, direction):
		#print("checking " + str([i, j]) + " in: " + str(direction) + " depth: " + str(depth))
		if depth == self.win_cond:
			return True
		if i > self.length - 1 or j > self.width - 1 or i < 0 or j < 0:
			return False
		if self.position[i][j] != player:
			return False
		return self.checkwin(depth + 1, i + direction[0], j + direction[1],
			player, direction)

	def check_win(self, player):
		visited = [[False for i in range(self.length)] for j in range (self.width)]
		options = [-1, 0, 1]
		win = False
		for i in range(self.length):
			for j in range(self.width):
				for x in options:
					for y in options:
						if [x, y] == [0, 0]:
							continue
						win = self.checkwin(0, i, j, player, [x, y])
						if win:
							return win
		return False

	def play(self, usr, Player):
		for i in range(self.width-1, -1, -1):
			if self.position[i][usr] == ' ':
				self.position[i][usr] = Player
				break

	def is_valid(self, usr):
		for i in range(self.width-1, -1, -1):
			if self.position[i][usr] == ' ':
				return True
		return False

	def max_in_row(self, depth, i, j, player, direction):
		#print("checking " + str([i, j]) + " in: " + str(direction) + " depth: " + str(depth))
		if i > self.length - 1 or j > self.width - 1 or i < 0 or j < 0:
			return -1
		if self.position[i][j] != player:
			return -1
		if depth == self.win_cond:
			return 1000
		return 1 + alpha*self.max_in_row(depth + 1, i + direction[0], j + direction[1],
			player, direction)

	def heuristic(self, player):
		#player with most in a row
		options = [-1, 0, 1]
		win = 0
		for i in range(self.length):
			for j in range(self.width):
				for x in options:
					for y in options:
						if [x, y] == [0, 0]:
							continue
						win = win + self.max_in_row(0, i, j, player, [x, y])
		return win

def run_game(length=6, width=6, win_cond=4):
	P = ['X', 'O']
	b = board(length, width, win_cond)
	ai = AI_player(P2, P1)
	turns = 0
	while(True):
		Player = P[turns % 2]
		print("Turn: " + str(turns))
		print("Player playing: " + Player)
		b.draw_board()
		if Player == P1:
			usr = input("select a row or [0] to exit: " + str([x+1 for x in range(length)]) + ": ")
			if not usr.isdigit():
				Player = P2
				continue
			usr = int(usr)
			if usr == 0:
				break
			if usr > b.length:
				Player = P2
				continue
			b.play(usr - 1, Player)
		else:
			value, usr = ai.make_move(b, MAX_DEPTH, Player)
			b.play(usr, Player)
		if b.check_win(Player):
			b.draw_board()
			print("Player: " + Player + " Wins!")
			break
		turns = turns + 1

def run_ai(length=6, width=6, win_cond=4):
	P = ['X', 'O']
	b = board(length, width, win_cond)
	ai = AI_player(P1, P2)
	ai2 = AI_player(P2, P1)
	turns = 0
	while(True):
		Player = P[turns % 2]
		print("Turn: " + str(turns))
		print("Player playing: " + Player)
		b.draw_board()
		if Player == P1:
			value, usr = ai.make_move(b, MAX_DEPTH, Player)
			b.play(usr, Player)
		else:
			value, usr = ai2.make_move(b, MAX_DEPTH, Player)
			b.play(usr, Player)
		if b.check_win(Player):
			b.draw_board()
			print("Player: " + Player + " Wins!")
			break
		if b.is_full():
			b.draw_board()
			print("Stalemate")
			break
		turns = turns + 1

run_ai(6,6,4)
