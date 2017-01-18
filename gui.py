from tkinter import *
import math
from Point2 import Point2
from random import randint
from convex_hull import ConvexHull
from typing import List
from convex_hull import sort_hulls
from convex_hull import divide_and_conquer_hulls

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
        self.canvas.grid(row=0, column=0, columnspan=6)
        self.canvas.bind("<Button-1>", self.callback_canvas_click)

        self.pending_points = []  # type: List[Point2]

        circle_button = Button(self.root, text='Generate circle', command=self.generate_circle).grid(row=1, column=0)
        polygon_button = Button(self.root, text='Generate polygon', command=self.generate_random_polygon).grid(row=1, column=1)
        merge_button = Button(self.root, text='Merge hulls', command=self.merge_hulls).grid(row=1, column=2)
        create_pending_button = Button(self.root, text='Create from pending points', command=self.create_from_pending).grid(row=1, column=3)
        route_button = Button(self.root, text='Calculate route through hulls', command=self.callback_route_button_click).grid(row=1, column=4)
        clear_button = Button(self.root, text='Clear canvas', command=self.callback_clear_button_click).grid(row=1, column=5)

        self.root.mainloop()

    def create_from_pending(self):
        self.hulls.append(divide_and_conquer_hulls(self.pending_points))
        self.pending_points = []
        self.redraw_hulls()

    def callback_route_button_click(self):
        self.path_through_hulls()

    def callback_clear_button_click(self):
        self.clear_canvas()
        self.clear_hulls()

    def callback_canvas_click(self, event):
        print("Press at " + str(event.x) + ", " + str(event.y))
        self.pending_points.append(Point2(event.x, event.y))
        self.canvas.create_oval(event.x - 2.5, event.y - 2.5, event.x + 2.5, event.y + 2.5, outline='orange', fill='orange')

    def path_through_hulls(self):
        print("Calculating path through hulls...")
        self.hulls = sort_hulls(self.hulls)

        for i in range(0, len(self.hulls)-1):

            hull_one = self.hulls[i]
            hull_two = self.hulls[i+1]

            self.canvas.create_line(hull_one.upper_hull[len(hull_one.upper_hull)-1].x, hull_one.upper_hull[len(hull_one.upper_hull)-1].y,
                                    hull_two.upper_hull[0].x,
                                    hull_two.upper_hull[0].y)

    def merge_hulls(self):

        merged_points = []

        for hull in self.hulls:
            merged_points.extend(hull.points)

        self.clear_canvas()
        self.clear_hulls()

        merged_hull = divide_and_conquer_hulls(merged_points)
        self.hulls.append(merged_hull)

        self.redraw_hulls()

    def clear_canvas(self):
        self.canvas.delete("all")

    def clear_hulls(self):
        self.hulls = []

    def generate_circle(self):
        points = []

        center = Point2(randint(10, self.WIDTH-100), randint(10, self.HEIGHT-100))
        radius = randint(50, self.HEIGHT / 4)

        radians = 0

        while radians < 2 * math.pi:
            points.append(Point2(center.x + (radius * math.cos(radians)), center.y + (radius * math.sin(radians))))
            radians += 0.1

        self.hulls.append(divide_and_conquer_hulls(points))
        self.redraw_hulls()

    def generate_random_polygon(self):
        points = []
        num_vertices = randint(10, 25)

        # Generate set of points
        for i in range(num_vertices):
            newPoint = Point2(randint(10, self.WIDTH - 50), randint(10, self.HEIGHT - 50))
            points.append(newPoint)

        self.hulls.append(divide_and_conquer_hulls(points))
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
            for p in range(0, len(convex_hull.upper_hull) - 1):
                self.canvas.create_line(convex_hull.upper_hull[p].x, convex_hull.upper_hull[p].y, convex_hull.upper_hull[p + 1].x,
                                        convex_hull.upper_hull[p + 1].y)

            # Connect the upper and lower hulls
            #    self.canvas.create_line(convex_hull.upper_hull[0].x, convex_hull.upper_hull[0].y, convex_hull.lower_hull[len(convex_hull.lower_hull) - 1].x,
            #                            convex_hull.lower_hull[len(convex_hull.lower_hull) - 1].y)


Gui()
