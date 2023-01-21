import numpy as np
import matplotlib.pyplot as plt
from typing import Union
from schelling import Schelling
from gaylord import Gaylord


class Visualization:
    def __init__(self, algorithm: Union[Schelling, Gaylord]) -> None:
        self.algorithm = algorithm
        self.initial_board = algorithm.board
        self.cmap = algorithm.city.cmap
        self.agents_ratio = algorithm.city.agents_ratio

    def show_results(self):
        fig = plt.figure(figsize=(11, 8), layout="constrained")
        spec = fig.add_gridspec(5, 13)

        ax0 = fig.add_subplot(spec[0:3, :6])
        ax0.imshow(self.initial_board, cmap = self.cmap)
        ax0.set_title(f'INITIAL STATE:  alfa={self.algorithm.a}, p={self.agents_ratio}')

        segregated_city = self.algorithm.run()
        ax1 = fig.add_subplot(spec[0:3, 4:12])
        im = ax1.imshow(segregated_city, cmap = self.cmap)
        ax1.set_title(f'SEGREGATED STATE  after {self.algorithm.n_steps} steps')
        fig.colorbar(im) 

        ax2 = fig.add_subplot(spec[3:, :])
        ax2.plot(np.arange(self.algorithm.n_steps), self.algorithm.average_si)
        ax2.set_xlabel('step')
        ax2.set_title('Average number of similar neighbours') 

        plt.savefig(f'visualizations/{self.algorithm.name}_{self.agents_ratio}_{self.algorithm.n_steps}.png')
        plt.show()     