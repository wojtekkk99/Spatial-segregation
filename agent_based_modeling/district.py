import numpy as np
from dataclasses import dataclass, field


@dataclass
class District():
    rases: list = field(default_factory=lambda: ['white', 'black'])
    salaries: list = field(default_factory=lambda: ['rich', 'poor']) 
    colors: list = field(default_factory=lambda: ['white', 'darkorange', 'navajowhite', 'darkcyan', 'mediumturquoise', 'purple', 'hotpink'])
    populations: dict = field(init=False)

    def __post_init__(self):
        self.populations = {(rase, salary): self.colors[2*i_r+i_s+1] for i_r, rase in enumerate(self.rases) for i_s, salary in enumerate(self.salaries)}

    def get_district_features(self) -> list:
        district_features = list(self.populations.keys())
        rases = np.array([district[0] for district in district_features])
        salaries = np.array([district[1] for district in district_features])
        return rases, salaries    

