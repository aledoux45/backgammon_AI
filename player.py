"""
Describes a player
"""

import numpy as np
from collections import deque
import random
from move import Moves
import torch


class Player:
    def __init__(self, player, random=False):
        self.player = player
        self.random = random

        ## NN
        self.hidden_units = 40
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.epsilon = 0.9  # exploration rate
        self.epsilon_min = 0.05 # min exploration rate
        self.epsilon_decay = 0.99 # 200
        self.learning_rate = 0.005
        self.gamma = 0.85  # discount rate -> 0.7 in paper
        self.memory = deque(maxlen=10000) # ~ last 100games of 100 moves
        self.model = self._build_model() if not self.random else None
        
    def roll(self):
        rolls = np.random.randint(1, 7, size=2)
        if rolls[0] == rolls[1]:
            return np.hstack([rolls, rolls]).tolist()
        else:
            return rolls.tolist()
            
    def _build_model(self):
        model = torch.nn.Sequential(
            torch.nn.Linear(52, self.hidden_units), # input = (N, H_in)
            torch.nn.ReLU(),
            torch.nn.Linear(self.hidden_units, 1),
        )
        return model

    def score(self, board):
        """
        Evaluates a board
        """
        nn_input = torch.FloatTensor(board.flat())
        score = self.model(nn_input)
        return score.item()

    def act(self, board, rolls):
        """
        legal_moves = List[Moves]
        """
        legal_moves = board.legal_moves(self.player, rolls)
        if len(legal_moves) == 0:
            return Moves([], rolls)
        elif len(legal_moves) == 1:
            return legal_moves[0]
        # add randomness of choice
        if np.random.random() < self.epsilon or self.random:
            choice = random.choice(legal_moves)
            return choice
        else: # choose board with highest score
            scores = []
            for move in legal_moves:
                next_board = board.step(self.player, move)
                score = self.score(next_board)
                scores.append(score)
            return legal_moves[np.argmax(scores)]

    # def remember(self, state, action, reward, new_state, done):
    #     self.memory.append([state, action, reward, new_state, done])

    def remember(self, state, reward, next_state, done):
        self.memory.append([state, reward, next_state, done]) # remember more next_states?

    def remember_game(self, board_history, winner, score):
        """
        winner = 0 or 1
        board_history = List[Board]
        score = 
        """
        for i in range(len(board_history)-1):
            if winner == self.player:
                # state, reward, next_state, done
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
        
    def replay(self, batch_size):
        loss_fn = torch.nn.MSELoss(reduction='sum')
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)

        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if len(self.memory) < batch_size: 
            return
        samples = random.sample(self.memory, batch_size)
        # boards = torch.cat([torch.FloatTensor(b.flat()) for b, r, next_b, d in samples])
        # next_boards = torch.cat([torch.FloatTensor(next_b.flat()) for b, r, next_b, d in samples])
        # rewards = torch.FloatTensor([r for b, r, next_b, d in samples])
        # targets = []
        # print("STH:", board.shape)
        # print("STH:", rewards.shape)
        
        for sample in samples:
            board, reward, next_board, done = sample
            if done:
                target = reward
            else:
                nn_input = torch.FloatTensor(next_board.flat())
                Q_future = self.model(nn_input)
                target = torch.FloatTensor([reward + Q_future.item() * self.gamma])
            
                # fit model
                self.model.train()  # set model to "training" mode (dropout ON)
                
                optimizer.zero_grad()
                
                nn_input = torch.FloatTensor(board.flat())
                out = self.model(nn_input)

                loss = loss_fn(out, target)
                # loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

                loss.backward()
                optimizer.step()

            # trail_loss += loss.item() ### IMPORTANT otherwise problem of memory leak
            # Regularization
            # if not self.config.bert and self.config.reg_lambda is not None:
            #     l2_reg = torch.tensor(0.)
            #     for W in model.parameters():
            #         if W.size(0) == 2:
            #             l2_reg += W.norm(2)
            #     loss += self.config.reg_lambda * l2_reg



    def load_model(self, filename):
        self.model = torch.load(filename)
        self.random = False
        self.epsilon = 0
        return self

    def save_model(self, outputfile):
        torch.save(self.model, outputfile)