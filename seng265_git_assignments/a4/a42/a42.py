#!/usr/bin/env python
"""
Assingmnet 4 Part 2
Created on Tuesday March 26 2024
@Author: Wesley Ducharme
@SID: V00974267
"""

import random
from typing import Dict, Tuple, Union

class PyArtConfig:
    """This class represents the configuration for a random shape
        Attributes
        ----------
            ranges: Dict[str, Tuple[Union[int, float], Union[int, float]]]
                A dict holding the shape parameters as the keys and their ranges for random number generation as the values
    """
    default_ranges: Dict[str, Tuple[Union[int, float], Union[int, float]]] = {# default range class variables
        'SHA': (0, 2),
        'RAD': (0, 100),
        'X': (0,700),
        'Y': (0, 500),
        'RX': (10, 30),
        'RY': (10, 30),
        'W': (10, 100),
        'H': (0, 100),
        'R': (0, 255),
        'G': (0, 255),
        'B': (0, 255),
        'OP': (0.0, 1.0)
    }

    def __init__(self, ranges: Dict[str, Tuple[Union[int, float], Union[int, float]]] = default_ranges):
        """Contructor for PyArtConfig class
            Parameters
            ----------
                ranges: Dict[str, Tuple[Union[int, float], Union[int, float]]]
                    the default ranges for the respective shape parameters
            Returns
            -------
                None
        """
        self.ranges = ranges

    def generate_random_numbers(self) -> Dict[str, Tuple[Union[int, float], Union[int, float]]]:
        """Populates a dictionary matching keys with randomly generated numbers within the given ranges
            Parameters
            ----------
                None
            Returns
            -------
                Dict[str, Tuple[Union[int, float], Union[int, float]]]
                    the populated dict
        """
        random_numbers: Dict[str, Tuple[Union[int, float], Union[int, float]]] = {}
        for key, (min_val, max_val) in self.ranges.items():
            if key == 'OP':
                random_numbers[key] = random.uniform(min_val, max_val)
            else:
                random_numbers[key] = random.randint(min_val, max_val)
        return random_numbers

class RandomShape:
    """This class represents a random shape
        Attributes
        ----------
            art_config: PyArtCongfig
                configuration parameters for the random shape
            cnt: int
                Count of the number of shapes
            shape_data: Dict[str, Tuple[Union[int, float], Union[int, float]]]
                randomized random data for the shape
    """
    def __init__(self, art_config: PyArtConfig, count: int):
        """Contructor for RandomShape class
            Parameters
            ----------
                art_config: PyArtConfig
                    Instance of PyArtConfig class
                count: int
                    value for the count of the number of shapes
            Returns
            -------
                None
        """
        self.art_config: PyArtConfig = art_config
        self.cnt: int = count
        self.shape_data: Dict[str, Tuple[Union[int, float], Union[int, float]]] = self.art_config.generate_random_numbers()

    def __str__(self) -> str:
        """Makes a string of the object data and returns it
            Parameters
            ----------
                None
            Returns
            -------
                str
                    the formatted string
        """
        return '\n'.join([f"{key}: {value}" for key, value in self.shape_data.items()])

    def as_Part2_line(self) -> str:
        """Makes a string representing a row of randomized shape information and returns it
            Parameters
            ----------
                None
            Returns
            -------
                str
                    string representation of the row
        """
        return f"{self.cnt:>3} {self.shape_data['SHA']:>3} {self.shape_data['X']:>3} " \
               f"{self.shape_data['Y']:>3} {self.shape_data['RAD']:>3} {self.shape_data['RX']:>3} " \
               f"{self.shape_data['RY']:>3} {self.shape_data['W']:>3} {self.shape_data['H']:>3} {self.shape_data['R']:>3} " \
               f"{self.shape_data['G']:>3} {self.shape_data['B']:>3} {self.shape_data['OP']:.1f}"

    def as_svg(self) -> str:
        """Makes an SVG string from the shape attributes
            Parameters
            ----------
                None
            Returns
            -------
                str
                    the SVG string
        """
        shape_type = self.shape_data['SHA']
        if shape_type == 0:  # Circle
            return f'<circle cx="{self.shape_data["X"]}" cy="{self.shape_data["Y"]}" r="{self.shape_data["RAD"]}" ' \
                   f'fill="rgb({self.shape_data["R"]}, {self.shape_data["G"]}, {self.shape_data["B"]})" fill-opacity="{self.shape_data["OP"]}" />'
        elif shape_type == 1:  # Rectangle
            return f'<rect x="{self.shape_data["X"]}" y="{self.shape_data["Y"]}" width="{self.shape_data["W"]}" height="{self.shape_data["H"]}" ' \
                   f'fill="rgb({self.shape_data["R"]}, {self.shape_data["G"]}, {self.shape_data["B"]})" fill-opacity="{self.shape_data["OP"]}" />'
        elif shape_type == 2:  # Ellipse
            return f'<ellipse cx="{self.shape_data["X"]}" cy="{self.shape_data["Y"]}" rx="{self.shape_data["RX"]}" ry="{self.shape_data["RY"]}" ' \
                   f'fill="rgb({self.shape_data["R"]}, {self.shape_data["G"]}, {self.shape_data["B"]})" fill-opacity="{self.shape_data["OP"]}" />'

def make_table(art_config: PyArtConfig) -> None:
    """Writes the table
        Parameters
        ----------
            art_config: PyArtConfig
                the configuration to use when making a RandomShape instance
        Returns
        -------
            None
    """
    art_config: PyArtConfig = PyArtConfig()
    cnt: int = 0
    print(f'CNT {"SHA"} {"  X"} {"  Y"} {"RAD"} {" RX"} {" RY"} {"  W"} {"  H"} {"  R"} {"  G"} {"  B"} {" OP"}')
    for number in range(10):
        random_shape: RandomShape = RandomShape(art_config, cnt)
        print(random_shape.as_Part2_line())
        cnt += 1

def main() -> None:
    """Main entry point of the program"""
    art_config: PyArtConfig = PyArtConfig()
    make_table(art_config)

if __name__ == "__main__":
    main()
