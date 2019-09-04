"""
Backgammon AI
"""

from environment import Environment
from player import Player
from datetime import datetime


def main():
    env = Environment()

    white = Player(0, env)
    black = Player(1, env)

    white_win = 0
    num_trials = 100
    t0 = datetime.now()

    for game in range(num_trials):
        env.reset()
        cur_board = env.board
        print(cur_board)

        board_history = []
        moves_history = []

        while not env.done:
            if env.player_to_move == 0:
                print("-- White:")
                roll = white.roll()
                print("roll:", roll)
                action = white.act(cur_board, roll)
                print("move:", action)
            else:
                print("-- Black:")
                roll = white.roll()
                print("roll:", roll)
                action = black.act(cur_board, roll)
                print("move:", action)

            board_history.append(env.board)
            moves_history.append(action)
            cur_board = env.step(action)

            print(cur_board)

        if env.winner == 0:
            white_win += 1
            print("White wins!")
        elif env.winner == 1:
            print("Black wins!")

        # Display game moves
        i=0
        while i < len(moves_history):
            if len(moves_history) == i+1:
                print(str(i) + "/ " + str(moves_history[i]))
            else:
                print(str(i) + "/ " + str(moves_history[i]) + "\t" + str(moves_history[i+1]))
            i+=2

        # Remember each board
        for i in range(len(board_history)-1):
            if env.winner == 0:
                white.remember(board_history[i], env.score_scale, board_history[i+1], False)
                black.remember(board_history[i], -env.score_scale, board_history[i+1], False)
            else:
                white.remember(board_history[i], -env.score_scale, board_history[i+1], False)
                black.remember(board_history[i], env.score_scale, board_history[i+1], False)
        if env.winner == 0:
            white.remember(board_history[-1], env.score_scale, None, True)
            black.remember(board_history[-1], -env.score_scale, None, True)
        else:
            white.remember(board_history[-1], -env.score_scale, None, True)
            black.remember(board_history[-1], env.score_scale, None, True)

        white.replay(32)
        black.replay(32)

    print("White wins percentage:", white_win/num_trials)
    print("Time:", datetime.now() - t0)

if __name__ == "__main__":
    main()