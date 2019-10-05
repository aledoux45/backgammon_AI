from flask import Flask, render_template, request
from os import environ
from board import Board
from move import Move
from player import Player
import numpy as np

app = Flask(__name__)

board = Board()
ai_can_move = False
ai = Player(1, random=False)
ai.load_model("run3/gen_10.h5")

@app.route('/')
def home():
    global board
    board = Board()
    ai_can_move = False
    return render_template("home.html")

@app.route('/game', methods=['GET','POST'])
def start_game():
    global board
    global ai_can_move
    # Your move, you are player 0
    if request.method == 'POST':
        player_move = request.form['move']
        # Check if valid entry:
        if "/" not in player_move:
            return render_template("game.html", board=board.render_ui(), error_message="Your move must be in the form of number/number such as 24/22")
        start = player_move.split("/")[0]
        finish = player_move.split("/")[1]
        blot = False
        start = 25 if start == "bar" else int(start)
        finish = 0 if finish == "off" else int(finish)
        roll = start - finish
        bearing_off = board.board[0, 7:].sum() == 0
        # Check if legal move:
        if start < 0 or start > 25 or finish < 0 or finish > 25:
            return render_template("game.html", board=board.render_ui(), error_message="Start and finish points must be in the interval [0,25]")
        if start <= finish:
            return render_template("game.html", board=board.render_ui(), error_message="Start point must be greater than finish point")
        elif roll > 6:
            return render_template("game.html", board=board.render_ui(), error_message="You cannot move a checker more than 6 points at a time (roll of dice)")
        elif start != 25 and board.board[0, 25] > 0:
            return render_template("game.html", board=board.render_ui(), error_message="You have a checker on the bar")
        elif board.board[0, start] == 0:
            return render_template("game.html", board=board.render_ui(), error_message="You don't have any checker on this point")
        elif not bearing_off and finish == 0:
            return render_template("game.html", board=board.render_ui(), error_message="You cannot bear off yet")
        elif board.board[1, 25-finish] > 1:
            return render_template("game.html", board=board.render_ui(), error_message="Your opponent has checkers on this point")
        # Check if blot
        if board.board[1, 25-finish] == 1:
            blot = True
        move = Move(start, roll, blot=blot)
        board = board.step(0, move)
        return render_template("game.html", board=board.render_ui(), error_message=None)
    # AI plays
    if ai_can_move:
        if board.is_game_over():
            return render_template("game.html", board=board.render_ui(), error_message="Game over!")
        roll = ai.roll()
        ai_action = ai.act(board, roll)
        for ai_move in ai_action:
            board = board.step(ai.player, ai_move)
    ai_can_move = True
    return render_template("game.html", board=board.render_ui(), error_message=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) # port=environ.get("PORT", 5000), 