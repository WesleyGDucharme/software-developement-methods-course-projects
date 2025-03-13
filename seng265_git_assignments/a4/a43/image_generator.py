#!/usr/bin/env python

"""
Assingmnet 4 Part 2
Created on Tuesday March 26 2024
@Author: Wesley Ducharme
@SID: V00974267
"""

import random as rd
from enum import Enum
from typing import IO, List, NamedTuple

class ShapeKind(str, Enum):
    """ShapeKind class describing supported shape kinds
        Attributes
        ----------
            None
    """
    CIRCLE = 0
    RECTANGLE = 1

    def __str__(self) -> str:
        """Returns a string of the variables values"""
        return f'{self.value}'

class Irange(NamedTuple):
    """Irange class holding integer range with minimum and maximum values
        Attributes
        ----------
            imin: int
                Integer's minimum
            imax: int
                Integer's maximum
    """
    imin: int
    imax: int

    def __str__(self) -> str:
        """Returns a string of the integer range"""
        return f'{self.imin},{self.imax}'

class Frange(NamedTuple):
    """Frange class holding float range with minimum and maximum values
        Attributes
        ----------
            fmin: float
                Float's minimum value
            fmax: float
                Float's maximum value
    """
    fmin: float
    fmax: float

    def __str__(self) -> str:
        """Returns a string of the float range"""
        return f'{self.fmin},{self.fmax}'

class Extent(NamedTuple):
    """Extent class based on width and height ranges
        Attributes
        ----------
            width: Irange
                Ranges for the width
            height: Irange
                Ranges for the height
    """
    width: Irange
    height: Irange

    def __str__(self) -> str:
        """Returns a string of the width and height ranges"""
        return f'({self.width},{self.height})'

class Color(NamedTuple):
    """RGB color definition based on integer ranges
        Attributes
        ----------
            red: Irange
                Range of values for red color intensity
            green: Irange
                Range of values for green color intensity
            blue: Irange
                Range of values for blue color intensity
            opacity: Frange
                Range of values for opacity
    """
    red: Irange
    green: Irange
    blue: Irange
    opacity: Frange

    def __str__(self) -> str:
        """Returns a string of the colors ranges"""
        return f'({self.red},{self.green},{self.blue})'

def gen_int(r: Irange) -> int:
    """Generates a random integer from an Irange class"""
    return rd.randint(r.imin, r.imax)

def gen_float(r: Frange) -> float:
    """Generates a random float from an Frange class"""
    return rd.uniform(r.fmin, r.fmax)

class PyArtConfig:
    """PyArtConfig class which is a configuration to guide the generation of a random shape
        Attributes
        ----------
            SHA: List[ShapeKind]
                list of ShapeKind instances
            CAN: Extent
                Instance of the Extent class holding the x and y ranges for the canvas
            RAD: Irange
                Instance of the Irange class holding the range for the radius of a circle
            RWH: Extent
                Instance of Extent class holding the width and height of a rectangle
            COL: Color
                Instance of Color class                
    """
    SHAPES: List[ShapeKind] = [ShapeKind.CIRCLE, ShapeKind.RECTANGLE]
    SHAPES_RANGE: Irange = Irange(0, len(SHAPES)-1)
    RAD_RANGE: Irange = Irange(0, 100)
    CAN_RANGES: Extent = Extent(Irange(0, 700), Irange(0, 500))
    RWH_RANGES: Extent = Extent(Irange(10, 100), Irange(0, 100))
    COL_RANGES: Color = Color(Irange(0, 255), Irange(0, 255), Irange(0, 255), Frange(0.0, 1.0))

    def __init__(self, sha: List[ShapeKind] = SHAPES, can: Extent = CAN_RANGES, rad: Irange = RAD_RANGE, rwh: Extent = RWH_RANGES, col: Color = COL_RANGES) -> None:
        """Initializes a configuration object"""
        self.SHA: List[ShapeKind] = sha
        self.CAN: Extent = can
        self.RAD: Irange = rad
        self.RWH: Extent = rwh
        self.COL: Color = col

    def __str__(self) -> str:
        """String representation of this configuration"""
        return f'\nUser-defined art configuration\n' \
               f'Shape types = ({", ".join(self.SHA)}\n)' \
               f'CAN(CXMIN,CXMAX,CYMIN,CYMAX) = {self.CAN}\n' \
               f'RAD(RADMIN,RADMAX) = ({self.RAD})\n' \
               f'RWH(WMIN,WMAX,HMIN,HMAX) = {self.RWH}\n' \
               f'COL(REDMIN,REDMAX,GREMIN,GREMAX,BLUMIN,BLUMAX) = {self.COL}\n' \
               f'COL(OPMIN,OPMAX) = ({self.COL.opacity.fmin:.1f},{self.COL.opacity.fmax:.1f})\n'

class RandomShape:
    """RandomShape class generateing a random shape specified by PyArtConfig    
        Attributes
        ----------
            config: PyArtConfig
                Configuration to guide the creation of the shape
            shape: List[Shapekind]
                list of the kinds of shapes to be made
            randpt: Tuple(int, int)
                Cordinates for random points
            rad: int
                Radius for circle
            rwh: Tuple(int, int)
                Width and height respectivly for a rectangle
            col: Color
                The configuration for a instance of the color class
    """
    def __init__(self, config: PyArtConfig) -> None:
        """Constructor for RectangleShape class
            Parameters
            ----------
                config: PyArtConfig
                    Configuration to guide the creation of the shape
            Returns
            -------
                None
        """
        self.config: PyArtConfig = config
        self.shape: List[ShapeKind] = rd.choice(config.SHAPES)
        self.randpt: Tuple(int, int) = (gen_int(config.CAN.width), gen_int(config.CAN.height))
        self.rad: int = gen_int(config.RAD)
        self.rwh: Tuple(int, int) = (gen_int(config.RWH.width), gen_int(config.RWH.height))
        self.col: Color = (gen_int(config.COL.red), gen_int(config.COL.green), gen_int(config.COL.blue), gen_float(config.COL.opacity))

class CircleShape:
    """A CircleShape class representing an SVG circle element
        Attributes
        ----------
            sha: int
                The shape identification number
            centx: int
                x cordinate of the circle's center
            centy: int
                y cordinate of the cricle's center
            rad: int
                The radius of the circle
            red: int
                The intensity of the color red
            gre: int
                The intensity of the color green
            blu: int
                The intensity of the color blue
            op: float
                The opacity of the shapes color
    """
    circle_count: int = 0

    @classmethod
    def get_circle_count(cls) -> int:
        return CircleShape.circle_count

    def __init__(self, rs: RandomShape) -> None:
        """Constructor for RectangleShape class
            Parameters
            ----------
                rs: RandomShape
                    Instance of a randomly generated shape
            Returns
            -------
                None
        """
        self.sha: int = 0
        self.centx: int = rs.randpt[0]
        self.centy: int = rs.randpt[1]
        self.rad: int = rs.rad
        self.red: int = rs.col[0]
        self.gre: int = rs.col[1]
        self.blu: int = rs.col[2]
        self.op: float = rs.col[3]

    def as_svg(self) -> str:
        """Svg string representation of a shape
            Parameters
            ----------
                None
            Returns
            -------
                str
                    The svg string
         """
        return f'<circle cx="{self.centx}" cy="{self.centy}" r="{self.rad}" ' \
               f'fill ="rgb({self.red},{self.gre},{self.blu})" ' \
               f'fill-opacity="{self.op}"></circle>'

    def __str__(self) -> str:
        """String representation of a shape
            Parameters
            ----------
                None
            Returns
            -------
                str
                    The string
         """
        return f'\nRandom Circle\n' \
               f'shape = {self.sha}\n' \
               f'radius = {self.rad}\n' \
               f'(centerx, centery) = ({self.centx},{self.centy})\n' \
               f'(red, green, blue) = ({self.red},{self.gre},{self.blu})\n' \
               f'opacity = {self.op:.1f}\n'

class RectangleShape:
    """A RectangleShape class representing an SVG rrectangle element
        Attributes
        ----------
            sha: int
                The shape identification number
            xpos: int
                x cordinate of the bottom left most corner
            ypos: int
                y cordinate of the bottom left most corner
            width: int
                The width of the rectangle
            height: int
                The height of the rectangle
            red: int
                The intensity of the color red
            gre: int
                The intensity of the color green
            blu: int
                The intensity of the color blue
            op: float
                The opacity of the shapes color
    """
    rect_count: int = 1

    @classmethod
    def get_rect_count(cls) -> int:
        """Returns the count of the rectangle"""
        return RectangleShape.rect_count

    def __init__(self, rs: RandomShape) -> None:
        """Constructor for RectangleShape class
            Parameters
            ----------
                rs: RandomShape
                    Instance of a randomly generated shape
            Returns
            -------
                None
        """
        self.sha: int = 1
        self.xpos: int = rs.randpt[0]
        self.ypos: int = rs.randpt[1]
        self.width: int = rs.rwh[0]
        self.height: int = rs.rwh[1]
        self.red: int = rs.col[0]
        self.gre: int = rs.col[1]
        self.blu: int = rs.col[2]
        self.op: float = rs.col[3]

    def as_svg(self) -> str:
        """Svg string representation of a shape
            Parameters
            ----------
                None
            Returns
            -------
                str
                    The svg string
         """
        return f'<rect x="{self.xpos}" y="{self.ypos}" width="{self.width}" ' \
               f'height="{self.height}" fill="rgb({self.red},{self.gre},{self.blu})" ' \
               f'fill-opacity="{self.op}"></rect>'

class HtmlDocument:
    """HtmlDocument Class representing an html document
        Attributes
        ----------
            title: str
                Title of the art
            file: IO 
                The file to open and write to
    """
    TAB: str = "   "
    def __init__(self, file_name: str, title: str):
        """Constructor for the HtmlDocument class
            Parameters
            ----------
                file_name: str
                    The name of the file to be made
                title: str
                    The title of the art to be generated
            Returns
            -------
                None
         """
        self.title: str = title
        self.__tabs: int = 0
        self.__file: IO = open(file_name, "w")
        self.__write_head()

    def increase_indent(self) -> None:
        """increases the number of tabs by 1
            Parameters
            ----------
                None
            Returns
            -------
                None
         """
        self.__tabs += 1

    def decrease_indent(self) -> None:
        """Decreases the number of tabs by 1
            Parameters
            ----------
                None
            Returns
            -------
                None
         """
        self.__tabs -= 1

    def append(self, content: str) -> None:
        """Writes a string to the html file
            Parameters
            ----------
                content: str
                    The content to be added
            Returns
            -------
                None
         """
        ts: str = HtmlDocument.TAB * self.__tabs
        self.__file.write(f'{ts}{content}\n')

    def __write_head(self) -> None:
        """Writes the head of the html file
            Parameters
            ----------
                None
            Returns
            -------
                None
         """
        self.append('<html>')
        self.append('<head>')
        self.increase_indent()
        self.append(f'<title>{self.title}</title>')
        self.decrease_indent()
        self.append('</head>')
        self.append('<body>')

    def __write_comment(self, comment: str) -> None:
        """Writes a comment in the specified format
            Parameters
            ----------
                comment: str
                    The comment to be made
            Returns
            -------
                None
         """
        self.append(f'   <!--{comment}-->')

    def open_svg_scope(self, dimensions: Extent) -> None:
        """Opens SVG preamble
            Parameters
            ----------
                dimensions: Extent
                    The length and width of the canvas's dimensions
            Returns
            -------
                None
         """
        self.__write_comment('Define and paint svg drawing box')
        self.append(f'   <svg width="{dimensions.width.imax}" height="dimensions.height.imax">')

    def write_tail(self) -> None:
        """Writes the end og the html file and closes the file
            Parameters
            ----------
                None
            Returns
            -------
                None
         """
        self.append('</body>')
        self.append('</html>')
        self.__file.close()

def make_random_shapes(config: PyArtConfig, num_shapes: int) -> List[RandomShape]:
    """Generates a random number of random shapes
        Parameters
        ----------
            config: PyArtConfig
                Configuration to guide the shapes generation
            num_shapes: int
                Number of shapes to generate
        Returns
        -------
            List[RandomShape]
                List of randomly generated shapes
     """
    shapes = []
    for i in range(num_shapes):
        rs = RandomShape(config)
        shapes.append(rs)
    return shapes

def make_file(config: PyArtConfig, filename: str) -> None:
    """Makes the html file and populates it with svg string representing shapes
        Parameters
        ----------
            config: PyArtConfig
                Configuration to guide the shapes generation
            filename: str
                Name of the file to write to
        Returns
        -------
            None
     """
    num_shapes = rd.randint(1, 10000)
    shapes = make_random_shapes(config, num_shapes)
    html_doc: HtmlDocument = HtmlDocument(filename, "Random Shapes")
    html_doc.open_svg_scope(config.CAN_RANGES)
    html_doc.increase_indent()
    html_doc.increase_indent()

    for rs in shapes:
        if rs.shape == ShapeKind.CIRCLE:
            shape = CircleShape(rs)
            html_doc.append(shape.as_svg())

        elif rs.shape == ShapeKind.RECTANGLE:
            shape = RectangleShape(rs)
            html_doc.append(shape.as_svg())

    html_doc.decrease_indent()
    html_doc.append("</svg>")
    html_doc.decrease_indent()
    html_doc.write_tail()

def main() -> None:
    """Main entry point for the program"""
    config: PyArtConfig = PyArtConfig()
    make_file(config, "a433.html")

if __name__ == "__main__":
    main()
