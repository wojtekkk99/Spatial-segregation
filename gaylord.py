import numpy as np
import random
from statistics import mean
from district import District
from city import City


class Gaylord:
    def __init__(self, city: City, district: District, a: int = 3, n_steps: int = 1000) -> None:
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
        self.n_populations = len(self.rases)
        self.board_size = self.periodic_board.shape[0]
        self.name = "Gaylord"


    def create_spaces_for_agents(self):
        agents_ready_to_move = []
        empty_spaces_for_agents = []
        for _ in range(self.n_populations):
            agents_ready_to_move.append([])
            empty_spaces_for_agents.append([])
        return agents_ready_to_move, empty_spaces_for_agents


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


    def get_valid_moves(self, agents_pos, empty_spaces):
        periodic_positions = {
            0: self.board_size-2,
            self.board_size-1: 1
        }
        moves = {}
        for population_id in range(self.n_populations):
            random.shuffle(empty_spaces[population_id])
            moves.update({pos: new_pos for pos, new_pos in zip(agents_pos[population_id], empty_spaces[population_id])})
        for pos, new_pos in moves.items():
            new_row, new_col = new_pos
            if new_row in periodic_positions.keys():
                new_row = periodic_positions[new_row]
            if new_col in periodic_positions.keys():
                new_col = periodic_positions[new_col]
            moves.update({pos: (new_row, new_col)})
        return moves


    def change_position(self, city, moves):
        for pos, new_pos in moves.items():
            value = city[pos[0], pos[1]]
            city[new_pos[0], new_pos[1]] = value
            city[pos[0], pos[1]] = -1
        return city


    def shorten_positions_list(self, agents_ready_to_move, empty_spaces_for_agents):
        for population_id in range(self.n_populations):
            n_agents = len(agents_ready_to_move[population_id])
            n_spaces = len(empty_spaces_for_agents[population_id])
            if n_agents > n_spaces:
                agents_ready_to_move[population_id] = random.sample(agents_ready_to_move[population_id], n_spaces)
            elif n_agents < n_spaces:
                empty_spaces_for_agents[population_id] = random.sample(empty_spaces_for_agents[population_id], n_agents) 
        return agents_ready_to_move, empty_spaces_for_agents


    def remove_duplicates(self, empty_spaces):
        choosen_positions = [space for id in range(len(empty_spaces)) for space in empty_spaces[id]]
        unique_pos, counts = np.unique(choosen_positions, return_counts=True, axis=0)
        same_pos = unique_pos[np.where(counts > 1)]
        same_pos = [tuple(new_pos) for new_pos in same_pos.tolist()]
        for id in range(len(empty_spaces)):
            for pos in same_pos:
                if pos in empty_spaces[id]:
                    empty_spaces[id].remove(pos)
        return empty_spaces  


    def run(self):
        for step in range(self.n_steps):  
            agents_ready_to_move, empty_spaces_for_agents = self.create_spaces_for_agents()
            for (row, col), _ in np.ndenumerate(self.periodic_board):
                if row != 0 and col != 0 and row != self.board_size-1 and col != self.board_size-1:
                    value = self.periodic_board[row, col]
                    neighborhood = self.periodic_board[
                        row - 1 : row + 2,
                        col - 1 : col + 2,
                    ]
                    if value != -1:    # agents
                        n_similar, n_similar_rase, n_similar_salary = self.find_n_similar(neighborhood, value)
                        self.si.append(n_similar)
                        # if n_similar < self.a and n_similar_rase < self.a_rase and n_similar_salary < self.a_salary:
                        if n_similar < self.a:   # without rase/salary similarities
                            agents_ready_to_move[value].append((row, col))
                    else:              # empty spaces
                        for population_id in range(self.n_populations):
                            n_similar, n_similar_rase, n_similar_salary = self.find_n_similar(neighborhood, population_id, True)
                            # if n_similar >= self.a or n_similar_rase >= self.a_rase or n_similar_salary >= self.a_salary:
                            if n_similar >= self.a:   # without rase/salary similarities
                                empty_spaces_for_agents[population_id].append((row, col))                
                             
            empty_spaces_for_agents = self.remove_duplicates(empty_spaces_for_agents)
            agents_ready_to_move, empty_spaces_for_agents = self.shorten_positions_list(agents_ready_to_move, empty_spaces_for_agents)

            valid_moves = self.get_valid_moves(agents_ready_to_move, empty_spaces_for_agents)
            if len(valid_moves) == 0:
                self.n_steps = step
                break
            self.periodic_board = self.change_position(self.periodic_board, valid_moves)

            segregated_board = self.periodic_board[1:self.board_size-1, 1:self.board_size-1]
            self.periodic_board = self.city.get_periodic(segregated_board)
            self.average_si.append(mean(self.si))
            
        return segregated_board