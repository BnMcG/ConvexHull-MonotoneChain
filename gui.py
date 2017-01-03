from tkinter import *
import math
from Point2 import Point2
from random import randint
from ConvexHull import ConvexHull
from typing import List


class Gui:
    NUM_POINTS = 15
    WIDTH=800
    HEIGHT=600

    hulls = []  # type: List[ConvexHull]

    def __init__(self):

        # Create a Tkinter window
        Tk.frame = LabelFrame
        self.root = Tk()
        self.root.wm_title("Convex Hull")

        # Create a canvas with a yellow background which is the same size as the window
        self.canvas = Canvas(self.root, bg="yellow", height=self.HEIGHT, width=self.WIDTH)
        self.canvas.grid(row=0, column=0, columnspan=4)

        circle_button = Button(self.root, text='Generate circle', command=self.generate_circle).grid(row=1, column=0)
        polygon_button = Button(self.root, text='Generate polygon', command=self.generate_random_polygon).grid(row=1, column=1)
        clear_button = Button(self.root, text='Clear canvas', command=self.clear_canvas).grid(row=1, column=2)
        merge_button = Button(self.root, text='Merge hulls', command=self.merge_hulls).grid(row=1, column=3)

        self.root.mainloop()

    def merge_hulls(self):

        merged_points = []

        for hull in self.hulls:
            merged_points.extend(hull.points)

        self.clear_canvas()

        merged_hull = ConvexHull(merged_points)
        self.hulls.append(merged_hull)

        self.redraw_hulls()

    def clear_canvas(self):
        self.hulls = []
        self.canvas.delete("all")

    def generate_circle(self):
        points = []

        center = Point2(self.WIDTH / 4, self.HEIGHT / 4)
        radius = randint(50, self.HEIGHT - (self.HEIGHT/2 - 10))

        radians = 0

        while radians < 2 * math.pi:
            points.append(Point2(center.x + (radius * math.cos(radians)), center.y + (radius * math.sin(radians))))
            radians += 0.1

        center = Point2((self.WIDTH / 4) * 2, (self.HEIGHT / 4) * 2)
        radius = randint(50, self.HEIGHT - (self.HEIGHT/2 - 10))
        radians = 0

        while radians < 2 * math.pi:
            points.append(Point2(center.x + (radius * math.cos(radians)), center.y + (radius * math.sin(radians))))
            radians += 0.1

        self.hulls.append(ConvexHull(points))
        self.redraw_hulls()

    def generate_random_polygon(self):
        points = []
        num_vertices = randint(10, 100)

        # Generate set of points
        for i in range(num_vertices):
            newPoint = Point2(randint(10, self.WIDTH - 10), randint(10, self.HEIGHT - 10))
            points.append(newPoint)

        self.hulls.append(ConvexHull(points))
        self.redraw_hulls()

    def redraw_hulls(self):

        self.canvas.delete("all")

        for convex_hull in self.hulls:
            # Create ovals on the canvas to represent each point
            for p in convex_hull.points:
                self.canvas.create_oval(p.x - 2.5, p.y - 2.5, (p.x + 2.5), (p.y + 2.5), outline='blue')

            # Overlay color for upper convex_hull
            for p in convex_hull.upper_hull:
                self.canvas.create_oval(p.x - 2.5, p.y - 2.5, (p.x + 2.5), (p.y + 2.5), outline='green', fill='green')

            # Overlay color for lower convex_hull
            for p in convex_hull.lower_hull:
                self.canvas.create_oval(p.x - 2.5, p.y - 2.5, (p.x + 2.5), (p.y + 2.5), outline='red', fill='red')

            # Connect points on the convex_hull with lines
            for p in range(0, len(convex_hull.hull) - 1):
                self.canvas.create_line(convex_hull.hull[p].x, convex_hull.hull[p].y, convex_hull.hull[p + 1].x,
                                        convex_hull.hull[p + 1].y)

            # Connect the upper and lower hulls
                self.canvas.create_line(convex_hull.upper_hull[0].x, convex_hull.upper_hull[0].y, convex_hull.lower_hull[len(convex_hull.lower_hull) - 1].x,
                                        convex_hull.lower_hull[len(convex_hull.lower_hull) - 1].y)


Gui()