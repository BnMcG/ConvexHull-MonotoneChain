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

        # Start at the third item in the list of points, as we just added the first
        # two to the upper hull manually, and we don't want to iterate over them
        # again
        for point in self.points:

            # If the upper hull contains more than two points and the last
            # three points don't make a right turn, delete the middle of the last
            # three points
            while len(self.upper_hull) >= 2:

                # Do the last three points make a right turn?
                # Essentially we can ignore the middle point and just see if
                # final point N is lower than point N-2

                # X1
                third_final_point = self.upper_hull[-2]

                # X2
                second_final_point = self.upper_hull[-1]

                turn = ConvexHull.calculate_turn(third_final_point, second_final_point, point)

                # If Z component of cross product is not negative, a right turn was NOT made
                if turn <= 0:
                    # Remove the point between the final point and the 3rd final point of the hull, as this point
                    # is actually inside the convex hull itself, not part of outlying hull.
                    self.upper_hull.pop()
                else:
                    break

            self.upper_hull.append(point)

    # Calculate the lower portion of the convex hull using the set of points given
    def calculate_lower_hull(self):
        print("Beginning lower hull calculation...")

        # Start three from the end of the list as we just added the final two points to the lower hull, and
        # then iterate backwards through the list
        for point in reversed(self.points):

            # If the lower hull contains more than two points and the last
            # three points don't make a right turn, delete the middle of the last
            # three points
            while len(self.lower_hull) >= 2:

                # Do the last three points make a right turn?
                # Essentially we can ignore the middle point and just see if
                # final point N is lower than point N-2

                # X1
                third_final_point = self.lower_hull[-2]

                # X2
                second_final_point = self.lower_hull[-1]

                turn = ConvexHull.calculate_turn(third_final_point, second_final_point, point)

                # If Z component of cross product is not negative, a right turn was NOT made
                if turn <= 0:
                    # Remove the 2nd to last point as it's inside the convex hull, and not part of the hull
                    # itself.
                    self.lower_hull.pop()
                else:
                    break

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

