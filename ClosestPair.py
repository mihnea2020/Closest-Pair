import math
import random
import pygame


WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Closest Pair")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (230, 30, 30)


class Point():
    COLOR = BLACK

    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)


def dist(p1, p2):
    return math.sqrt(((p2[1]-p1[1])**2)+((p2[0]-p1[0])**2))


def brute_force(points):
    min_dist = float("inf")
    p1 = None
    p2 = None
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            d = dist(points[i], points[j])
            if d < min_dist:
                min_dist = d
                p1 = points[i]
                p2 = points[j]
    return p1, p2, min_dist


def rec(xsorted, ysorted):
    n = len(xsorted)
    if n <= 3:
        return brute_force(xsorted)
    else:
        midpoint = xsorted[n//2]
        xsorted_l = xsorted[:n//2]
        xsorted_r = xsorted[n//2:]
        ysorted_l = []
        ysorted_r = []
        for point in ysorted:
            ysorted_l.append(point) if (
                point[0] <= midpoint[0]) else ysorted_r.append(point)
        (p1_l, p2_l, delta_l) = rec(xsorted_l, ysorted_l)
        (p1_r, p2_r, delta_r) = rec(xsorted_r, ysorted_r)
        (p1, p2, delta) = (p1_l, p2_l, delta_l) if (
            delta_l < delta_r) else (p1_r, p2_r, delta_r)
        in_band = [point for point in ysorted if midpoint[0] -
                   delta < point[0] < midpoint[0]+delta]
        for i in range(len(in_band)):
            for j in range(i+1, min(i+7, len(in_band))):
                d = dist(in_band[i], in_band[j])
                if d < delta:
                    #print(in_band[i], in_band[j])
                    (p1, p2, delta) = (in_band[i], in_band[j], d)
        return p1, p2, delta


def closest(points):
    xsorted = sorted(points, key=lambda point: point[0])
    ysorted = sorted(points, key=lambda point: point[1])
    return rec(xsorted, ysorted)


def main():
    WIN.fill(WHITE)
    pointNumber = 50
    points = [(0,0)] * pointNumber

    for i in range(pointNumber):
        pointX = random.randint(5, 595)
        pointY = random.randint(5, 395)
        points[i] = (pointX, pointY)
        point = Point(pointX, pointY,2)
        point.draw(WIN)
        pygame.display.update()

    print(points)
    print(closest(points))

    pygame.draw.line(WIN, RED, closest(points)[0], closest(points)[1], 2)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            pygame.display.update()

    pygame.QUIT


if __name__ == "__main__":
    main()
