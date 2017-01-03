from typing import List
from Point2 import Point2


class ConvexHull:

    def __init__(self, points: List[Point2]):
        self.points = points
        self.hull = []  # type: List[Point2]
        self.upper_hull = []  # type: List[Point2]
        self.lower_hull = []  # type: List[Point2]

        # Points must be sorted before convex hull generation can take place
        self.points = self.sort_points(self.points)

        self.calculate_upper_hull()
        self.calculate_lower_hull()
        self.merge_hulls()

    # If this method returns 0 it means no turn was made and points are collinear
    # if this method returns a +ve number, a left turn was made
    # if this method returns a -ve number ,a right turn was made
    @staticmethod
    def calculate_turn(p1: Point2, p2: Point2, p3: Point2):
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

    # Sort points by x coordinate
    # Python3 supports type hinting and it's BEAUTIFUL!
    def sort_points(self, list_of_points: List[Point2]):

        # Bubble sort? Everybody <3 bubble sort
        for r in range(len(list_of_points) - 1):
            # If we reach the end of the loop below without this variable changing to true that means no swaps were
            # performed and we can break out of the loop
            swap_performed = False

            for iteration in range(len(list_of_points) - 1):
                current_point = list_of_points[iteration]
                next_point = list_of_points[iteration + 1]

                if current_point.x > next_point.x:
                    temp = list_of_points[iteration]
                    list_of_points[iteration] = list_of_points[iteration + 1]
                    list_of_points[iteration + 1] = temp
                    swap_performed = True

            if not swap_performed:
                break

        return list_of_points

    # Calculate the upper portion of the convex hull using the set of points given
    def calculate_upper_hull(self):
        print("Beginning upper hull calculation...")

        for point in self.points:
            while len(self.upper_hull) >= 2 and ConvexHull.calculate_turn(self.upper_hull[-2], self.upper_hull[-1], point) <= 0:
                self.upper_hull.pop()

            self.upper_hull.append(point)

    # Calculate the lower portion of the convex hull using the set of points given
    def calculate_lower_hull(self):
        print("Beginning lower hull calculation...")

        # This time we work from the
        for point in reversed(self.points):
            while len(self.lower_hull) >= 2 and ConvexHull.calculate_turn(self.lower_hull[-2], self.lower_hull[-1], point) <= 0:
                self.lower_hull.pop()

            self.lower_hull.append(point)


    # Merge the upper and lower portions to form one cohesive convex hull
    def merge_hulls(self):
        # Remove the first and last points from the lower hull, as there will be overlap with the
        # upper hull
        self.lower_hull.remove(self.lower_hull[len(self.lower_hull) - 1])
        self.lower_hull.remove(self.lower_hull[0])

        self.hull = self.upper_hull
        self.hull.extend(self.lower_hull)
        #self.hull = self.sort_points(self.hull)

