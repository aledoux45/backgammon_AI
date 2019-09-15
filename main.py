"""
Backgammon AI
"""

from environment import Environment
from player import Player
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt


def main():
    env = Environment()

    white = Player(0, env)
    black = Player(1, env)
    # random_black = Player(1, env, random=True)

    num_games = 5000
    num_test_games = 20
    test_frequency = 100
    generation_frequency = 1000
    
    performance = defaultdict(list)
    generation = 0

    t0 = datetime.now()

    for game in range(num_games):
        # Save generation
        if game % generation_frequency == 0: # Save generation
            print("Saving generation", str(generation))
            white.save_model("models/gen_"+str(generation)+".h5")
            black.save_model("models/gen_"+str(generation)+".h5")
            generation += 1

        # Check performance
        if game % test_frequency == 0:
            print("Testing current generation")
            reference_black = Player(1, env, random=True)
            for gen in range(generation):
                reference_black.load_model("models/gen_"+str(gen)+".h5")
                performance[gen].append(env.check_performance(white, reference_black, num_test_games))
        
        # Play game
        env.play_game(white, black, verbose=False)

        # Remember the game
        white.remember_game(env.board_history, env.winner, env.score)
        black.remember_game(env.board_history, env.winner, env.score)

        # Replay boards from the past
        white.replay(250)
        black.replay(250)

        print("Game", game, " | Nb moves", len(env.board_history), " | winner", env.winner)

    # Save last generation        
    print("Saving generation", str(generation))
    white.save_model("models/gen_"+str(generation)+".h5")
    black.save_model("models/gen_"+str(generation)+".h5")

    # Plot performance evolution
    for gen in performance:
        plt.plot(performance[gen], label="Gen"+str(gen))
    plt.ylim((0,1))
    plt.xlabel("Test")
    plt.ylabel("Performance")
    plt.title("Evolution of performance of last generation player vs older generations")
    plt.legend()
    plt.grid()
    plt.savefig("plots/perfEvolution.png")

    # Final output
    print("Success evolution:", performance)
    print("Time:", datetime.now() - t0)


if __name__ == "__main__":
    main()