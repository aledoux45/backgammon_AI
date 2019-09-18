"""
Describes a player
"""

import numpy as np
from collections import deque
import random
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam
from move import Moves


class Player:
    def __init__(self, player, env, random=False):
        self.player = player
        self.env = env
        self.random = random
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001
        self.gamma = 0.85
        self.memory = deque(maxlen=2000)
        self.model = self._build_model() if not self.random else None
        
    def roll(self):
        roll = np.random.randint(1, 7, size=2)
        if roll[0] == roll[1]:
            return np.hstack([roll, roll])
        else:
            return roll
            
    def _build_model(self):
        model = Sequential()
        state_shape = self.env.board.board.reshape(-1).shape
        # print("Shape:",state_shape)
        model.add(Dense(40, input_shape=state_shape, activation="tanh"))
        # model.add(Dense(24, activation="tanh"))
        # model.add(Dense(24, activation="tanh"))
        model.add(Dense(1))
        model.compile(loss="mean_squared_error", optimizer=Adam(lr=self.learning_rate))
        # model.add(Dense(4, activation="softmax"))
        # model.compile(optimizer='rmsprop',
        #               loss='categorical_crossentropy',
        #               metrics=['accuracy'])
        model.summary()
        return model

    def act(self, board, rolls):
        legal_moves = board.legal_moves(self.player, rolls)
        if len(legal_moves) == 0:
            return Moves([], rolls)
        # add randomness of choice

        if np.random.random() < self.epsilon or self.random:
            choice = random.sample(legal_moves, 1)[0]
            return choice
        else: # choose board with highest score
            scores = []
            for lm in legal_moves:
                for move in lm:
                    next_board = board.step(self.player, move)
                score = self.model.predict(next_board.flat())[0][0]
                # print("LM:", lm)
                # print("Score:", score)
                scores.append(score)
            return legal_moves[np.argmax(scores)]

    # def remember(self, state, action, reward, new_state, done):
    #     self.memory.append([state, action, reward, new_state, done])

    def remember(self, state, reward, next_state, done):
        self.memory.append([state, reward, next_state, done])

    def remember_game(self, board_history, winner, score):
        # winner = 0 or 1
        # board_history = list of Board objects
        for i in range(len(board_history)-1):
            if winner == self.player:
                self.remember(board_history[i], score, board_history[i+1], False)
                # self.remember(board_history[i].flip(), -score, board_history[i+1].flip(), False)
            else:
                self.remember(board_history[i], -score, board_history[i+1], False)
                # self.remember(board_history[i].flip(), score, board_history[i+1].flip(), False)
        # last board        
        if winner == self.player:
            self.remember(board_history[-1], score, None, True)
            # self.remember(board_history[-1].flip(), -score, None, True)
        else:
            self.remember(board_history[-1], -score, None, True)
            # self.remember(board_history[-1].flip(), score, None, True)
        
    def replay(self, batch_size=32):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
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

    def load_model(self, filename):
        self.model = load_model(filename)
        self.random = False
        self.epsilon = 0

    def save_model(self, outputfile):
        self.model.save(outputfile)