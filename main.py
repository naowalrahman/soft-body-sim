from vpython import *
import math

G: float = 9.81
PRESSURE: float = 10
DT: float = 0.1

class Point2d:
    def __init__(self) -> None:
        # z-component isn't use but is required by vpython
        self.pos = vector(0, 0, 0)
        self.vel = vector(0, 0, 0)
        self.force = vector(0, 0, 0)

class Spring:
    def __init__(self, beg: Point2d, end: Point2d) -> None:
        # points
        self.beg: Point2d = beg
        self.end: Point2d = end

        # rest length
        self.length: float = (end.pos - beg.pos).mag

        # normal vector, to be set
        self.nx: float = 0
        self.ny: float = 0
        
class SoftBody:
    def __init__(self, points: list[Point2d], springs: list[Spring], point_mass: float, kS: float, kD: float) -> None:
        self.n: int = len(points)
        self.point_mass: float = point_mass
        self.points: list[Point2d] = points
        self.springs: list[Spring] = springs
        self.kS: float = kS
        self.kD: float = kD

    def update(self) -> None:
        for point in self.points:
            point.force.y = self.point_mass * G

        for spring in self.springs:
            beg, end = spring.beg, spring.end
            p1, p2 = beg.pos, end.pos
            dist = (p1 - p2).mag

            if dist != 0:
                dvx = beg.vel.x - end.vel.x
                dvy = beg.vel.y - end.vel.y

                force = (dist - spring.length) * self.kS + (beg.vel - end.vel).dot((p1 - p2) / dist) * self.kD
            
            