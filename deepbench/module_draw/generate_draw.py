# TODO: comments

__all__ = ['create_line', 'create_arc', 'create_circle', 'create_rectangle',
           'create_regular_polygon']


import numpy as np
from math import pi, acos, cos, sin
from matplotlib.patches import Wedge, Rectangle, RegularPolygon
from matplotlib.path import Path



def _patch2im(thepatch, imshape):
    """
    Helper function for Patches to convert to a numpy.array

    :param thepatch: matplotlib.Patch object to be converted
        :type: numpy.array
    :param imshape: numpy.array to be the receiver of the patch
    :return: array object representation of patch
        :type: numpy.array
    """
    x = np.arange(1, imshape.shape[0])
    y = np.arange(1, imshape.shape[1])
    g = np.meshgrid(x, y)

    coords = np.array(list(zip(*(c.flat for c in g))))

    elpath = Path(thepatch.get_verts())

    validcoords = elpath.contains_points(coords)
    ellipsepoints = coords[validcoords]

    outim = np.zeros(imshape.shape)
    outim[ellipsepoints[:,0],ellipsepoints[:,1]] = 1

    return outim


def create_rectangle(imshape, xy, width, height, angle=0.0, fill=True):
    """

    :param imshape: image that rectangle will be drawn in
        :type: numpy.array
    :param xy: Lower left corner of rectangle
        :type: Tuple(float,float)
    :param width: x-dimension of the rectangle
        :type: float
    :param height: y-dimension of the rectangle
        :type: float
    :param angle: angle of rectangle
        :type: float
    :param fill: Fill rectangle shape
        :type: boolean
    :return:
        numpy.array that includes rectangle
    """
    rect = Rectangle(xy, width, height, angle=angle, fill=fill)
    return _patch2im(rect,imshape)


def create_regular_polygon(imshape, xy, angle=0.0, vertices=3, radius=1, fill=True):
    """
    Create a regular polygon with a specified number of sides.
    :param imshape: Image that the polygon will be drawn in.
        :type: numpy.array
    :param xy: Lower-left corner of polygon.
        :type: Tuple(float, float)
    :param angle: Rotation of polygon
        :type: float
    :param vertices: number of vertices in polygon
        :type: int
    :param radius: The distance from the center to each of the vertices
        :type: float
    :param fill: Fill polygon
        :type: boolean
    :return:
    """
    toRadians = angle*pi/180.0
    polyg = RegularPolygon(xy, vertices, radius, orientation=toRadians,fill=fill)
    return _patch2im(polyg, imshape)


def create_arc(imshape, center, radius, width, theta1,theta2):
    """

    :param imshape: image object to receive arc object
        :type: numpy.array
    :param center: focal point of drawn arc.
        :type: Tuple(float,float)
    :param radius: distance from the center to arc
        :type: float
    :param width: thickness of the arc
        :type: float
    :param theta1: Start of subtended arc
        :type: float
    :param theta2: End of subtended arc
        :type: float
    :return: numpy.array with arc in the object.
    """
    arc = Wedge(center, radius, theta1, theta2, width)
    return _patch2im(arc, imshape)


def create_circle(imshape, center, radius, width):
    """
    :param imshape: image object to receive circle object
        :type: numpy.array
    :param center: focal point of drawn arc.
        :type: Tuple(float,float)
    :param radius: distance from the center to arc
        :type: float
    :param width: thickness of the arc
        :type: float
    """
    return create_arc(imshape, center, radius,
                      width=width, theta1=0, theta2=360)


def create_line(imshape, start, end,  linewidth=1):
    #create a line using Rectangle, interpolate ending position
    hyp = ( (end[1]-start[1])**2 + (end[0]-start[0])**2 )**0.5
    angle = acos( (end[0]-start[0]) / hyp)


    x_shift = linewidth/2.0 * cos((pi-angle))
    y_shift = linewidth/2.0 * sin((pi-angle))
    xy_start = (start[0] + x_shift, start[1] + y_shift)
    xy_end = (end[0] + x_shift, end[1]+y_shift)

    height_rect = linewidth
    width_rect = ( (xy_end[1]-xy_start[1])**2 + (xy_end[0]-xy_start[0])**2 )**0.5
    angle_deg = angle*180.0/pi
    rect = Rectangle(xy_start, width=width_rect,height=height_rect, angle=angle_deg)

    return _patch2im(rect, imshape)



