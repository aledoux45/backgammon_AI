"""
Describes a player
"""

import numpy as np
from collections import deque
import random
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from move import Moves


class Player:
    def __init__(self, player, env):
        self.player = player
        self.env = env
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.gamma = 0.85
        self.memory = deque(maxlen=2000)
        self.model = self._build_model()

    def roll(self):
        roll = np.random.randint(1, 7, size=2)
        if roll[0] == roll[1]:
            return np.hstack([roll, roll])
        else:
            return roll
            
    def _build_model(self):
        model = Sequential()
        state_shape = self.env.board.board.reshape(-1).shape
        print("Shape:",state_shape)
        model.add(Dense(24, input_shape=state_shape, activation="tanh"))
        model.add(Dense(24, activation="tanh"))
        model.add(Dense(24, activation="tanh"))
        model.add(Dense(1))
        model.compile(loss="mean_squared_error", optimizer=Adam(lr=self.learning_rate))

        model.summary()
        return model

    def act(self, board, rolls):
        legal_moves = board.legal_moves(self.player, rolls)
        if len(legal_moves) == 0:
            return Moves([], rolls)
        # add randomness of choice
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            choice = random.sample(legal_moves, 1)[0]
            return choice
        else: # choose board with highest score
            scores = []
            for lm in legal_moves:
                for move in lm:
                    next_board = board.step(self.player, move)
                score = self.model.predict(next_board.flat())[0][0]
                print("LM:", lm)
                print("Score:", score)
                scores.append(score)
            return legal_moves[np.argmax(scores)]

    # def remember(self, state, action, reward, new_state, done):
    #     self.memory.append([state, action, reward, new_state, done])

    def remember(self, state, reward, next_state, done):
        self.memory.append([state, reward, next_state, done])
        
    def replay(self, batch_size=32):
        if len(self.memory) < batch_size: 
            return
        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            board, reward, next_board, done = sample
            if done:
                target = reward
            else:
                Q_future = self.model.predict(next_board.flat())[0][0]
                target = reward + Q_future * self.gamma
            self.model.fit(board.flat(), np.array([[target]]), epochs=1, verbose=0)