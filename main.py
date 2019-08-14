"""
Backgammon AI
"""

from environment import Environment
from player import Player


def main():
    env = Environment()
    print(env.board)
    print(env.player_to_move)

    white = Player()
    black = Player()

    # while not env.done:
    #     if env.white_to_move:
    #         action = white.action(env)
    #     else:
    #         action = black.action(env)
    #     env.step(action)
    #     if env.num_halfmoves >= config.play.max_game_length:
    #         env.adjudicate()

    # gamma   = 0.9
    # epsilon = .95

    # trials  = 100
    # trial_len = 500 # cap the number of rolls per game

    # white = Player(config, pipes=pipes)
    # black = Player(config, pipes=pipes)

    # while not env.done:
    #     if env.white_to_move:
    #         action = white.action(env)
    #     else:
    #         action = black.action(env)
    #     env.step(action)
    #     if env.num_halfmoves >= config.play.max_game_length:
    #         env.adjudicate()

    # if env.winner == Winner.white:
    #     black_win = -1
    # elif env.winner == Winner.black:
    #     black_win = 1
    # else:
    #     black_win = 0

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