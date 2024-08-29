#!/usr/bin/env python

"""
Assingmnet 4 Part 1
Created on Tuesday March 26 2024
@Author: Wesley Ducharme
@SID: V00974267
"""

from typing import IO, Union

from typing import NamedTuple


class CircleShape:
    """This class represents a circle
        Attributes
        ---------- 
            cx: int
                x cordinate of the circle's center
            cy: int
                y cordinate of the circle's center
            rad: int
                radius of the circle
            red: int
                intensity of the color red
            green: int
                intensity of the color green
            blue: int 
                intensity of the color blue
            op: float
                opacity of the shapes color
    """

    def __init__(self, cx: int, cy: int, rad: int, red: int, gre: int, blu: int, op: float):
        """Constructor for RectangleShape class
            Parameters
            ----------
                cx: int
                    Value for cx
                cy: int
                    Value for cy
                rad: int
                    value for rad
                red: int
                    value for intensity of the color red
                gre: int
                    value for the intensity of the color green
                blu: int 
                    value for the intensity of the color blue
                op: float
                    value for the opacity of the shapes color
            Returns
            -------
                None 
        """
        self.cx: int = cx
        self.cy: int = cy
        self.rad: int = rad
        self.red: int = red
        self.green: int = gre
        self.blue: int = blu
        self.op: float = op

    def svg_render(self) -> str:
        """Renders the attributes of the shape to a SVG string
            Parameters
            ----------
                None
            Returns
            -------
                str
                    The SVG string
        """
        return f'      <circle cx="{self.cx}" cy="{self.cy}" r="{self.rad}" fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></circle>'


class RectangleShape:
    """This class represents a rectangle
        Attributes
        ---------- 
            xpos: int
                x cordinate of the left most corner
            ypos: int
                y cordinate of the left most corner
            width: int
                width of the rectangle
            height: int
                height of the rectangle
            red: int
                intensity of the color red
            green: int
                intensity of the color green
            blue: int 
                intensity of the color blue
            op: float
                opacity of the shapes color
    """
                
    def __intit__(elf, x: int, y: int, width: int, height: int, red: int, gre: int, blu: int, op: float):
        """Constructor for RectangleShape class
            Parameters
            ----------
                x: int
                    Value for xpos
                y: int
                    Value for ypos
                width: int
                    value for the width of the rectangle
                height: int
                    value for the height of the rectangle
                red: int
                    value for intensity of the color red
                gre: int
                    value for the intensity of the color green
                blu: int 
                    value for the intensity of the color blue
                op: float
                    value for the opacity of the shapes color
            Returns
            -------
                None 
        """
        self.xpos: int = x
        self.ypos: int = y
        self.width: int = width
        self.height: int = height
        self.red: int = red
        self.green: int = gre
        self.blue: int = blu
        self.op: float = op

    def svg_render(self) -> str:
        """Renders the attributes of the shape to a SVG string
            Parameters
            ----------
                None
            Returns
            -------
                str
                    The SVG string
        """
        return f'      <rect x="{self.xpos}" y="{self.ypos}" width="{self.width}" \
                 height="{self.height}" fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></rect>'

class HtmlDocument:
    """This class represents a html document
        Attributes
        ----------
            title: str
                Title of the art
            file: IO
                The file to write to
        """
    TAB: str = "   "
    def __init__(self, file_name: str, title: str):
        """Constructor for SvgCanvas class
            Parameters
            ----------
                file_name: str
                    Name of the file to write to
                title: str
                    Title of the art
            Returns
            -------
                None
        """
        self.title: str = title
        self.__tabs: int = 0
        self.__file: IO = open(file_name, "w")
        self.__write_head()

    def increase_indent(self) -> None:
        """Increases the number of tabs by one
            Parameters
            ----------
                None
            Returns
            -------
                None
        """
        self.__tabs += 1

    def decrease_indent(self) -> None:
        """Decreases the number of tabs by one
            Parameters
            ----------
                None
            Returns
            -------
                None
        """
        self.__tabs -= 1

    def append(self, content: str) -> None:
        """Appends a string to the document
            Parameters
            ----------
                content: str
                    The string to append
            Returns
            -------
                None
        """
        ts: str = HtmlDocument.TAB * self.__tabs
        self.__file.write(f'{ts}{content}\n')

    def __write_head(self) -> None:
        """Writes the head of the html code to the document
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
        """Appends a comment to the document in the specified format
            Parameters
            ----------
                comment: str
                    The comment being added
            Returns
            -------
                None
        """
        self.append(f'<!--{comment}-->')

    def __write_tail(self) -> None:
        """Writes the tail of the html code to the document
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

class SvgCanvas:
    """This class represents a canvas made of Svg strings
        Attributes
        ----------
            width: int
                Width of the canvas
            height: int
                Height of the canvas
            shapes: List[Union[CircleShape, RectangleShape]]
                List of the shapes that will populate the canvas
    """
    TAB: str = "   "

    def __init__(self, width: int, height: int):
        """Constructor for SvgCanvas class
            Parameters
            ----------
                width: int
                    The value for the width of the canvas
                height: int
                    The value for the height of the canvas
            Returns
            -------
                None
        """
        self.width: int = width
        self.height: int = height
        self.shapes: List[Union[CircleShape, RectangleShape]] = []

    def add_shape(self, shape: Union[CircleShape, RectangleShape]):
        """Adds a shape to the canvas
            Parameters
            ----------
                shape: Union[CircleShape, RectangleShape]
                    The shape class to add
            Returns
            -------
                None
        """
        self.shapes.append(shape)

    def gen_art(self) -> str:
        """Generates an SVG string
            Parameters
            ----------
                None
            Returns
            -------
                str
                    SVG string generated
        """
        svg_content: str = ""
        for shape in self.shapes:
            svg_content += shape.svg_render() + "\n"
        return f"<svg width=\"{self.width}\" height=\"{self.height}\">\n{svg_content}{SvgCanvas.TAB}</svg>"

def make_canvas() -> SvgCanvas:
    """Makes a SvgCanvas and populates it
        Parameters
        ----------
            None
        Returns
        -------
            SvgCanvas
                Instance of a SvgCanvas class
    """

    canvas: SvgCanvas = SvgCanvas(500, 300)
    canvas.add_shape(CircleShape(50, 50, 50, 255, 0, 0, 1.0))
    canvas.add_shape(CircleShape(150, 50, 50, 255, 0, 0, 1.0))
    canvas.add_shape(CircleShape(250, 50, 50, 255, 0, 0, 1.0))
    canvas.add_shape(CircleShape(350, 50, 50, 255, 0, 0, 1.0))
    canvas.add_shape(CircleShape(450, 50, 50, 255, 0, 0, 1.0))
    canvas.add_shape(CircleShape(50, 250, 50, 0, 0, 255, 1.0))
    canvas.add_shape(CircleShape(150, 250, 50, 0, 0, 255, 1.0))
    canvas.add_shape(CircleShape(250, 250, 50, 0, 0, 255, 1.0))
    canvas.add_shape(CircleShape(350, 250, 50, 0, 0, 255, 1.0))
    canvas.add_shape(CircleShape(450, 250, 50, 0, 0, 255, 1.0))
    return canvas

def make_file(canvas: SvgCanvas, filename: str) -> None:
    """Makes a html file
        Parameters
        ----------
            canvas: SvgCanvas, required
                Body of the html code made of SVG strings.
            filename: str, required
                Name of the file to write to.
        Returns
        -------
            None
               
    """
    doc: HtmlDocument = HtmlDocument(filename, "My Art")
    doc.increase_indent()
    doc._HtmlDocument__write_comment("Define SVG drawing box")
    doc.append(canvas.gen_art())
    doc.decrease_indent()
    doc._HtmlDocument__write_tail()


def main() -> None:
    """Main entry point of the program"""
    canvas: SvgCanvas = make_canvas()
    make_file(canvas, "a41.html")

if __name__ == "__main__":
    main()
