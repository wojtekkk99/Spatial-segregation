from district import District
from city import City
from schelling import Schelling
from gaylord import Gaylord
from visualization import Visualization


if __name__ == "__main__":
    district = District()
    city = City(district, size=80, agents_ratio=0.5)

    # Gaylord algorithm
    gaylord = Gaylord(city, district, a=3)
    visualization = Visualization(gaylord)
    visualization.show_results()

    # Schelling algorithm
    # schelling = Schelling(city, district, a=4, n_steps=8000)
    # visualization = Visualization(schelling)
    # visualization.show_results()