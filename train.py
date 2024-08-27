"""
Backgammon AI
"""

from environment import Environment
from player import Player
from board import Board
from move import Move, Moves
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import os
import torch


def train():
    env = Environment()

    white = Player(0)
    black = Player(1)
    # random_black = Player(1, env, random=True)

    total_num_games = 500
    num_test_games = 20
    test_frequency = 10
    generation_frequency = 100
    outputfolder = "run_test"
    
    os.makedirs(outputfolder, exist_ok=True)
    performance = defaultdict(dict)
    generation = 0

    t0 = datetime.now()

    for game in range(total_num_games):
        # Save generation
        if game % generation_frequency == 0: # Save generation
            print("Saving generation", str(generation))
            white.save_model(outputfolder+"/gen_"+str(generation)+".model")
            black.save_model(outputfolder+"/gen_"+str(generation)+".model")
            generation += 1

        # Check performance
        if game % test_frequency == 0:
            print("Testing current generation")
            reference_black = Player(1, random=False)
            for gen in range(generation):
                reference_black.load_model(outputfolder+"/gen_"+str(gen)+".model")
                performance[gen][game] = env.check_performance(white, reference_black, num_test_games)
        
        # Play game
        env.play_game(white, black, verbose=False)

        # Remember the game
        white.remember_game(env.board_history, env.winner, env.score)
        black.remember_game(env.board_history, env.winner, env.score)

        # Replay boards from the past
        white.replay(100) # ~ 1 whole game of 100 moves
        black.replay(100)

        print("Game", game, " | Nb moves", len(env.board_history), " | winner", env.winner, " | score", env.score)

    # Save last generation        
    print("Saving generation", str(generation))
    white.save_model(outputfolder+"/best.model")
    black.save_model(outputfolder+"/best.model")

    # Plot performance evolution
    for gen in performance:
        plt.plot(list(performance[gen].keys()), list(performance[gen].values()), label="Gen"+str(gen))
    plt.ylim((0,1))
    plt.xlabel("Game")
    plt.ylabel("Performance")
    plt.title("Evolution of performance of player vs other generations")
    plt.legend()
    plt.grid()
    plt.savefig(outputfolder+"/perfEvolution.png")

    # Final output
    print("Time:", datetime.now() - t0)


if __name__ == "__main__":
    # train()
    # env = Environment()

    # white = Player(0)
    # black = Player(1)

    # env.play_game(white, black, verbose=True)

    # train()

    ######## Best opening moves
    # if you roll a 3-1 -> 8/5 6/5
    # if you roll a 4-2 -> 8/4 6/4
    # if you roll a 5-3 -> 8/4 6/4
    
    # Load best player
    best_player = Player(0, random=False)
    best_player.load_model("run_test/best.model")
    
    board = Board()
    print("Starting board:", best_player.score(board))

    # 3-1
    legal_moves = board.legal_moves(best_player.player, [3,1])
    for move in legal_moves:
        print(move)
        score = best_player.score(board.step(best_player.player, move))
        print("Starting board + 3/1:", score)
        print()

    # # 4-2
    # legal_moves = board.legal_moves(best_player.player, [4,2])
    # for move in legal_moves:
    #     print(move)
    #     score = best_player.score(board.step(best_player.player, move))
    #     print("Starting board + 4/2:", score)
    #     print()

    # # 5-3
    # legal_moves = board.legal_moves(best_player.player, [5,3])
    # for move in legal_moves:
    #     print(move)
    #     score = best_player.score(board.step(best_player.player, move))
    #     print("Starting board + 5/3:", score)
    #     print()