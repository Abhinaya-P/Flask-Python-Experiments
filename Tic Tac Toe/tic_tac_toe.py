from flask import Flask
from flask import render_template
from flask import request
import random
import copy

app = Flask(__name__)
players_board = []
players_board.append('')

chosen = {}
chosen['player'] = None
chosen['computer'] = None
chosen['match_over'] = False

def chooseRandomMoveFromList(l):
	random.shuffle(l)
	return l

def get_next_move():
	board_dup = copy.copy(players_board)
	letter = chosen['computer']
	opponent = chosen['player']
	corners = [1,3,7,9]
	sides = [2,4,6,8]
	#Look for a winning position
	for i in range(1,10):
		if isFreeSpot(i):
			board_dup[i] = letter
			if isWinner(board_dup,letter):
				return i
			board_dup[i] = '-'
				
	#Block the opponent from winning
	for i in range(1,10):
		if isFreeSpot(i):
			board_dup[i] = opponent
			if isWinner(board_dup,opponent):
				return i
			board_dup[i] = '-'
	
	
	#Choose from corners
	corners = chooseRandomMoveFromList(corners)
	for i in corners:
		if isFreeSpot(i):
			return i
		
	#choose the center	
	if(isFreeSpot(5)):
		return 5
	
	#Choose the sides
	sides = chooseRandomMoveFromList(sides)
	for i in sides:
		if isFreeSpot(i):
			return i
	
	return -1
	
def isBoardFull():
	for x in range(1,10):
		if players_board[x] == '-':
			return False
	return True
	
def isFreeSpot(move):
	return players_board[move] == '-'

def isWinner(p_board,le):
	return ((p_board[1] == le and p_board[4] == le and p_board[7] == le) or
		   (p_board[2] == le and p_board[5] == le and p_board[8] == le) or
		   (p_board[3] == le and p_board[6] == le and p_board[9] == le) or
		   (p_board[1] == le and p_board[2] == le and p_board[3] == le) or
		   (p_board[4] == le and p_board[5] == le and p_board[6] == le) or
		   (p_board[7] == le and p_board[8] == le and p_board[9] == le) or
		   (p_board[1] == le and p_board[5] == le and p_board[9] == le) or
		   (p_board[3] == le and p_board[5] == le and p_board[7] == le))

		   

for x in range(1,10):
	players_board.append('-')

@app.route("/")
def index():
	return render_template("tic_tac_toe.html")
	
@app.route("/board",methods=['GET'])
def board():
	chosen['player'] = request.args['player']
	if chosen['player'] == 'X':
		chosen['computer'] = 'O'
	else:
		chosen['computer'] = 'X'
	return render_template("board.html",moves=players_board)
	
@app.route("/play",methods=['GET'])
def play():
	players_board[0] = ''
	move = int(request.args['move'])
	if isFreeSpot(move) and chosen['match_over'] is False:
		players_board[move] = chosen['player']
		if isWinner(players_board,chosen['player']):
		   players_board[0] = "Congratulations !!You have won the game."
		   chosen['match_over'] = True
		elif isBoardFull():
			if isWinner(players_board,chosen['computer']):
				players_board[0] = "Computer has won the game!!"
				chosen['match_over'] = True
			else:
				chosen['match_over'] = True
				players_board[0] = "Match is a DRAW!"
	else:
		players_board[0] = "Invalid Move!!"
	return render_template("board.html",moves=players_board)
	
@app.route("/computer")
def computer():
	final_choice = get_next_move()
	if final_choice != -1:
		players_board[final_choice] = chosen['computer']
		if isWinner(players_board,chosen['computer']):
			chosen['match_over'] = True
			players_board[0] = "Computer has won the game!!"
		elif isBoardFull():
			if isWinner(players_board,chosen['player']):
				chosen['match_over'] = True
				players_board[0] = "Congratulations !!You have won the game."
			else:
				chosen['match_over'] = True
				players_board[0] = "Match is a DRAW!"
	return render_template("board.html",moves=players_board)
	

if __name__ == "__main__":
	app.run(debug=True)
