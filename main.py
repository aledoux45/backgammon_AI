"""
Backgammon AI
"""

from environment import Environment
from player import Player


def main():
    env = Environment()

    white = Player(0)
    black = Player(1)

    white_win = 0

    for game in range(100):
        env.reset()
        print(env.board)
        while not env.done:
            if env.player_to_move == 0:
                print("-- White:")
                roll = white.roll()
                print("roll:", roll)
                action = white.act(env.board, roll)
                print("move:", action)
            else:
                print("-- Black:")
                roll = white.roll()
                print("roll:", roll)
                action = black.act(env.board, roll)
                print("move:", action)
            env.step(action)
            print(env.board)

        if env.winner == 0:
            white_win += 1
            print("White wins!")
        elif env.winner == 1:
            print("Black wins!")
        else:
            raise ValueError("No winner")

    print("White wins percentage:", white_win/100)
    # black.finish_game(black_win)
    # white.finish_game(-black_win)

    # data = []
    # for i in range(len(white.moves)):
    #     data.append(white.moves[i])
    #     if i < len(black.moves):
    #         data.append(black.moves[i])

    # cur.append(pipes)
    
    # for trial in range(trials):
    #     # cur_state = env.reset().reshape(1,2)
    #     cur_state = env.reset()
    #     done = False
    #     while not done:
    #         # player 1
    #         action = player1.act(cur_state)
    #         new_state, reward, done, _ = env.step(action)

    #         # reward = reward if not done else -20
    #         # new_state = new_state.reshape(1,2)
    #         player1.remember(cur_state, action, reward, new_state, done)
            
    #         player1.replay()       # internally iterates default (prediction) model
    #         player1.target_train() # iterates target model

    #         cur_state = new_state

    #         # player 2
    #         action = player1.act(cur_state)
    #         new_state, reward, done, _ = env.step(action)

    #         # reward = reward if not done else -20
    #         # new_state = new_state.reshape(1,2)
    #         player1.remember(cur_state, action, reward, new_state, done)
            
    #         player1.replay()       # internally iterates default (prediction) model
    #         player1.target_train() # iterates target model

    #         cur_state = new_state


if __name__ == "__main__":
    main()