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
    random_black = Player(1, env)

    num_games = 10000
    num_test_games = 100
    performance = []

    t0 = datetime.now()

    for game in range(num_games):
        if game % 10 == 0: # check performance
            success = 0
            for test_game in range(num_test_games):
                env.play_game(white, random_black)
                success += env.loser
            performance.append(success/num_test_games)
        else:
            env.play_game(white, black)

        # Remember the game
        white.remember_game(env.board_history, env.winner, env.score)
        black.remember_game(env.board_history, env.winner, env.score)

        # Replay game from the past
        white.replay(32)
        black.replay(32)

    white.save_model("models/model1.h5")
    black.save_model("models/model2.h5")
    print("Success evolution:", performance)
    print("Time:", datetime.now() - t0)

        # env.reset()
        # cur_board = env.board
        # print(cur_board)

        # board_history = []
        # moves_history = []

        # while not env.done:
        #     if env.player_to_move == 0:
        #         print("-- White:")
        #         roll = white.roll()
        #         print("roll:", roll)
        #         action = white.act(cur_board, roll)
        #         print("move:", action)
        #     else:
        #         print("-- Black:")
        #         roll = white.roll()
        #         print("roll:", roll)
        #         action = black.act(cur_board, roll)
        #         print("move:", action)

        #     board_history.append(env.board)
        #     moves_history.append(action)
        #     cur_board = env.step(action)

        #     print(cur_board)

        # if env.winner == 0:
        #     white_win += 1
        #     print("White wins!")
        # elif env.winner == 1:
        #     print("Black wins!")

        # # Display game moves
        # i=0
        # while i < len(moves_history):
        #     if len(moves_history) == i+1:
        #         print(str(i) + "/ " + str(moves_history[i]))
        #     else:
        #         print(str(i) + "/ " + str(moves_history[i]) + "\t" + str(moves_history[i+1]))
        #     i+=2


if __name__ == "__main__":
    main()