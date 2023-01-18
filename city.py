import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from district import District


class City:
    def __init__(self, district: District, size: int = 70, agents_ratio: float = 0.8) -> None:
        self.district = district
        self.size = size
        self.agents_ratio = agents_ratio

    def set_params(self):
        self.district.extract_populations()
        populations = self.district.populations
        self.n_agents = len(populations)
        agent_colors = list(populations.values())
        agent_colors.insert(0, self.district.colors[0])
        self.cmap = ListedColormap(agent_colors)

    def generate_board(self):
        empty_ratio = (1 - self.agents_ratio)
        indices = np.arange(-1, self.n_agents)
        prob = np.full(self.n_agents+1, self.agents_ratio/self.n_agents)
        prob[0] = empty_ratio
        board = np.random.choice(indices, size=self.size*self.size, p=prob)
        board = np.reshape(board, (self.size, self.size))
        return board

    def show_board(self, board):
        plt.figure(figsize=(8,8))
        plt.imshow(board, cmap = self.cmap)
        plt.show()

    def get_periodic(self, board):
        n = board.shape[0]
        first_col = board[:, 0]
        first_row = board[0, :]
        last_col = board[:, n-1]
        last_row = board[n-1, :]
        left_offset = np.insert(first_col, 0, board[n-1, 0])
        left_offset = np.insert(left_offset, left_offset.shape[0], board[0, 0])
        right_offset = np.insert(last_col, 0, board[n-1, n-1])
        right_offset = np.insert(right_offset, right_offset.shape[0], board[0, n-1])
        periodic_board =  np.concatenate(([last_row], board), axis=0)
        periodic_board =  np.concatenate((periodic_board, [first_row]), axis=0)
        periodic_board = np.concatenate((np.array([right_offset]).T, periodic_board), axis=1)
        periodic_board = np.concatenate((periodic_board, np.array([left_offset]).T), axis=1)
        return periodic_board