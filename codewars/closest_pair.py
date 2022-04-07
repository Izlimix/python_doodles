import math
from itertools import takewhile

"""
  Problem statement: https://www.codewars.com/kata/5376b901424ed4f8c20002b7
  Given a list of points, return the pair of points that are closest together.
  Not the most optimal approach to this problem, see https://en.wikipedia.org/wiki/Closest_pair_of_points_problem

  The below solution is a doodle to understand Sweep Line Algorithms in general.
  This code solves the kata on the site just fine, though small optimisations could definitely be made.
  The kata does not seem to consider points of >2 dimensions (x, y, ...), however I believe this should still work on those.
  Distance used here is Euclidean distance a^2 + b^2 = c^2.
  - Manhattan distance can be substituted in without problem.
  - Other metrics will need to consider whether storing the points within d of the x-coord is admissible.
"""

def closest_pair(points):
    # Sweep line approach overview:
    # Consider each point p from left-to-right (ascending x)
    #   Keeping track of the min dist seen so far (d)
    #     and the recently-seen points within d of p,
    #   Check the distance of p from each recently seen point
    #     (can skip points whose |y - py| > d)

    # Sort points by coordinates (x, y, ...)
    points = sorted(points)

    # init with the first two points, just crash if we have fewer than 2
    (p1, p2) = (points[0], points[1])
    d = math.dist(p1, p2)
    # Keep recents in insertion order to consider fewer elements when removing, as the points have already been sorted
    recents = dict.fromkeys((p1, p2))

    for p in points[2:]:
        (x, *_) = p
        # Forget distant points
        #   takewhile, so you don't need to check the entire set if it fails early
        #   List, to avoid changing recents while iterating over it
        forget = list(takewhile(lambda point: (x - point[0]) >= d, recents))
        for point in forget:
            del recents[point]

        for r in recents:
            # Check the distance from p to each recent point
            # todo: skip points that are > d away in any dimension y...?
            distance = math.dist(p, r)
            if distance < d:
                # New shortest line!
                (p1, p2) = (r, p)
                d = distance

        # Add p to the set of recently-seen points
        recents[p] = None

    return (p1, p2)
