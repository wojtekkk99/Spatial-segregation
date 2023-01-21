import numpy as np
import random
import matplotlib.pyplot as plt
from statistics import mean
from matplotlib.colors import ListedColormap
from district import District
from city import City


class Schelling:
    def __init__(self, city: City, district: District, a: int = 4, n_steps: int = 8000) -> None:
        self.city = city
        self.district = district
        self.a = a
        self.n_steps = n_steps
    
        self.a_rase = a+2
        self.a_salary = a+2
        self.si = []
        self.average_si = []
        self.board = self.city.generate_board()
        self.periodic_board = self.city.get_periodic(self.board)
        self.rases, self.salaries = self.district.get_district_features()


    def choose_new_position(self, empty_houses, row, col, board_size):
        periodic_positions = {
            0: board_size-2,
            board_size-1: 1
        }
        random_house = random.choice(empty_houses)
        new_row = row + random_house[0] - 1
        if new_row in periodic_positions.keys():
            new_row = periodic_positions[new_row]
        new_col = col + random_house[1] - 1
        if new_col in periodic_positions.keys():
            new_col = periodic_positions[new_col]
        return new_row, new_col


    def get_valid_moves(self, moves):
        new_positions = [n_pos for _, n_pos in moves.items()]
        unique_pos, counts = np.unique(new_positions, return_counts=True, axis=0)
        same_pos = unique_pos[np.where(counts > 1)]
        same_pos = [tuple(new_pos) for new_pos in same_pos.tolist()]
        valid_moves = {pos:new_pos for pos, new_pos in moves.items() if new_pos not in same_pos} 
        return valid_moves   
        

    def find_n_similar(self, neighborhood, value, empty_space=False):
        rase, salary = self.rases[value], self.salaries[value]
        same_rase_idx = np.where(self.rases == rase)[0]
        same_salary_idx = np.where(self.salaries == salary)[0]  
        if empty_space: 
            n_similar = len(np.where(neighborhood == value)[0])
        else: 
            n_similar = len(np.where(neighborhood == value)[0]) - 1
        n_similar_rase = 0
        n_similar_salary = 0
        for idx_r in same_rase_idx:
            if idx_r != value:
                n_similar_rase = len(np.where(neighborhood == idx_r)[0]) 
        for idx_s in same_salary_idx:
            if idx_s != value:
                n_similar_salary = len(np.where(neighborhood == idx_s)[0])  
        return n_similar, n_similar_rase, n_similar_salary


    def run(self):
        for step in range(self.n_steps):  
            moves = {}
            for (row, col), _ in np.ndenumerate(self.periodic_board):
                n = self.periodic_board.shape[0]
                if row != 0 and col != 0 and row != n-1 and col != n-1:
                    value = self.periodic_board[row, col]
                    if value != -1:    # -1 -> empty space
                        neighborhood =self.periodic_board[
                            row - 1 : row + 2,
                            col - 1 : col + 2,
                        ]
                        n_similar, n_similar_rase, n_similar_salary = self.find_n_similar(neighborhood, value)
                        self.si.append(n_similar)
                        if n_similar < self.a and n_similar_rase < self.a_rase and n_similar_salary < self.a_salary:
                            empty_houses = list(
                                zip(
                                    np.where(neighborhood == -1)[0], np.where(neighborhood == -1)[1]
                                )
                            )
                            if len(empty_houses) != 0:
                                new_row, new_col = self.choose_new_position(empty_houses, row, col, n)
                                moves[(row, col)] = (new_row, new_col)

            valid_moves = self.get_valid_moves(moves)
            for pos, new_pos in valid_moves.items():
                value = self.periodic_board[pos[0], pos[1]]
                self.periodic_board[new_pos[0], new_pos[1]] = value
                self.periodic_board[pos[0], pos[1]] = -1

            segregated_board = self.periodic_board[1:n-1, 1:n-1]
            self.periodic_board = self.city.get_periodic(segregated_board)
            self.average_si.append(mean(self.si))
            if step%2000 == 0: print(f'step: {step}, mean si: {mean(self.si)}')

        return segregated_board