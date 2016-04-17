'''
INTRUCTIONS:
- LEFT-CLICK to add a free point to the demo contrain rigid-body
- RIGHT-CLICK to add a fixed point to the demo contrain rigid-body
- MIDDLE-CLICK to add a box rigid body
- SCROLL to add a free moving body
- X to clear the canvas
'''

import pygame
from pygame import gfxdraw
import random
import time
import math

pygame.init()

class canvas:
    def __init__(self, width, height, windowCaption):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(windowCaption)

def drawText(text, fontSize, x, y):
    font = pygame.font.SysFont(None, fontSize)
    TextSurf = font.render(text, True, (224 / 4, 247 / 4, 255 / 4))
    TextRect = TextSurf.get_rect()
    TextRect.x = x;
    TextRect.y = y;
    screen.surface.blit(TextSurf, TextRect)


# GLOBAL VARIABLES
#g = pygame.math.Vector2(0, -9.81)
G = 6.674 * 10 ** (-11)
screen = canvas(700, 500, "Newton's Laboratory - Simulation")
fps = float("inf")  # uncapped

# PREPERENCES
pixelsPerMetre = 50
keepBodiesInScreen = True

bodies = []
class Body:
    anchored = False
    parent = None
    colour = (255, 165, 0)
    elasticity = 1

    def __init__(self, x, y, m=1, r=10):
        self.displacement = pygame.math.Vector2(x, y)
        self.previousDisplacement = pygame.math.Vector2(x, y)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.radius = r
        self.mass = m
        bodies.append(self)

    def velocity(self):
        return self.displacement - self.previousDisplacement

    def kineticEnergy(self):
        return 0.5 * self.mass * self.velocity().length_squared()

    def gravitationalPotentialEnergy(self):
        GPE = 0
        for other in bodies:
            if self is other:
                break
            separation = (self.displacement - other.displacement).length()
            if separation > 0:
                GPE += G * self.mass * other.mass / (self.displacement - other.displacement).length()
        return GPE

    def energy(self):
        return self.kineticEnergy() + self.gravitationalPotentialEnergy()

    def volume(self):
        return 4/3*math.pi*self.radius**3

    def density(self):
        return self.mass/self.volume()

    def simulate(self, dt):
        self.acceleration *= dt ** 2
        p = 2 * self.displacement - self.previousDisplacement + self.acceleration
        self.previousDisplacement = self.displacement
        self.displacement = p
        self.acceleration *= 0

    def accelerate(self, acceleration):
        self.acceleration += acceleration

    def applyForce(self, force):
        self.acceleration += force / self.mass

    def gravitationalForce(self, other):
        if self.displacement == other.displacement:
            return pygame.math.Vector2(0, 0)
        separation = self.displacement - other.displacement
        return G * self.mass * other.mass * separation.normalize() / separation.length_squared()

    def collide(self, other, dt):

        '''
        d = self.displacement- other.p

        length = d.length()
        lengthLimit = self.r + other.r

        if length < lengthLimit:
            v1 = self.displacement- self.pp
            v2 = other.displacement- other.pp
            if not length == 0:
                factor = 0.5*((length-lengthLimit)/length)
            else:
                factor = lengthLimit/2

            if not self.anchored:
                self.displacement-= d*factor
            if not other.anchored:
                other.displacement+= d*factor

            damping = (self.e+other.e)/2

            if preserve_impulse and length != 0:
                f1 = (damping*(d*v1))/(length)**2
                f2 = (damping*(d*v2))/(length)**2

                v1 += f2*d - f1*d
                v2 += f1*d - f2*d

                self.pp = self.displacement- v1
                other.pp = other.displacement- v2
        '''

        separation = self.displacement - other.displacement
        lengthLimit = self.radius + other.radius

        if not (0 < separation.dot(separation) <= lengthLimit ** 2):
            return False

        contactForce = (separation.normalize() * lengthLimit - separation) / dt ** 2

        self.applyForce(contactForce)
        other.applyForce(-contactForce)

        return True

    def constraintCollide(self, constraint, dt):
        '''Q = self.displacement# Centre of circle
        r = self.r+3+(self.p-self.pp).length() #Radius of circle
        startPointVector = constraint.point1.displacement# Start of line segment
        lineVector = constraint.point2.displacement- startPointVector # Vector along the line

        a = lineVector.dot(lineVector)
        b = 2 * lineVector.dot(startPointVector - Q)
        c = startPointVector.dot(startPointVector) + Q.dot(Q) - 2 * startPointVector.dot(Q) - r**2
        disc = b**2 - 4 * a * c
        if disc < 0 or a == 0:
            return False, None
        else:
            sqrt_disc = math.sqrt(disc)
            t1 = (-b + sqrt_disc)/(2*a)
            t2 = (-b - sqrt_disc)/(2*a)

        if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
            return False, None

        scalarParameter = max(0, min(1, -b/(2*a)))

        if (startPointVector + scalarParameter*lineVector - Q).length() <= r:
            i = startPointVector + scalarParameter*lineVector
        else:
            return False, None

        d = self.displacement- i

        pygame.gfxdraw.filled_circle(screen.surface, int(d.x), int(d.y), 5, (0,0,0))

        return True, i'''

        startPointVector = constraint.pointA.displacement
        lineVector = constraint.pointB.displacement - startPointVector
        circleCentreVector = self.displacement

        if lineVector.dot(lineVector) == 0:
            return False

        scalarParameter = lineVector.dot(circleCentreVector - startPointVector) / lineVector.dot(lineVector)

        scalarParameter = min(max(0, scalarParameter), 1)

        closestPoint = startPointVector + lineVector * scalarParameter

        displacementFromCircle = closestPoint - circleCentreVector

        if not (0 < displacementFromCircle.length_squared() < self.radius ** 2):
            return False

        meanMass = (self.mass + constraint.pointA.mass + constraint.pointB.mass) / 3

        normalForce = meanMass * (displacementFromCircle.normalize() * self.radius - displacementFromCircle) / dt ** 2

        # self.displacement-= ((closestPoint-circleCentreVector)/(closestPoint-circleCentreVector).length())*(self.r-(closestPoint-circleCentreVector).length())

        self.applyForce(-normalForce)

        constraint.pointA.applyForce((1 - scalarParameter) * normalForce)
        constraint.pointB.applyForce(scalarParameter * normalForce)

        return True

    def borderCollide(self, dt):
        '''
        if not self.r < self.p.x < screen.width-self.r:
            self.p.x = 2*self.pp.x-self.p.x-self.a.x
        if not self.r < self.p.y < screen.height-self.r:
            self.p.y = 2*self.pp.y-self.p.y-self.a.y


        self.p.x = max(self.p.x, self.r)
        self.p.x = min(self.p.x, screen.width-self.r)
        self.p.y = max(self.p.y, self.r)
        self.p.y = min(self.p.y, screen.height-self.r)
        '''

        normalForce = pygame.math.Vector2(0, 0)
        if self.displacement.x < self.radius:
            normalForce.x += (self.radius - self.displacement.x) / dt ** 2
        if self.displacement.x + self.radius > screen.width:
            normalForce.x -= (self.displacement.x + self.radius - screen.width) / dt ** 2
        if self.displacement.y < self.radius:
            normalForce.y += (self.radius - self.displacement.y) / dt ** 2
        if self.displacement.y + self.radius > screen.height:
            normalForce.y -= (self.displacement.y + self.radius - screen.height) / dt ** 2

        self.accelerate(normalForce)

    def draw(self):
        pygame.gfxdraw.filled_circle(screen.surface, int(self.displacement.x), int(self.displacement.y), int(self.radius), self.colour)
        pygame.gfxdraw.aacircle(screen.surface, int(self.displacement.x), int(self.displacement.y), int(self.radius),self.colour)

class Planet(Body):
    def __init__(self, m, r, h=10):
        Body.__init__(self, screen.width / 2, screen.height + r - h, m, r)
        self.colour = (0, 255, 0)
        self.h = h

    def draw(self):
        pygame.draw.rect(screen.surface, self.colour, (0, screen.height - self.h, screen.width, self.h))

points = []
class Point(Body):
    radius = 6

    def __init__(self, x, y, m=0.5):
        Body.__init__(self, x, y, m, 5)
        self.displacement = pygame.math.Vector2(x, y)
        self.previousDisplacement = pygame.math.Vector2(x, y)
        self.acceleration = pygame.math.Vector2(0, 0)
        points.append(self)

    def correct(self, distance):
        self.displacement += distance


class fixedPoint(Point):
    anchored = True
    colour = (204, 0, 204)

    def accelerate(self, force):
        pass

    def simulate(self, dt):
        pass

    def correct(self, distance):
        pass


constraints = []
class Constraint:
    forceConstant = 0.4
    parent = None
    colour = (165, 165, 165)

    def __init__(self, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB
        self.target = pointA.displacement.distance_to(self.pointB.displacement)
        constraints.append(self)

    def elasticPotentialEnergy(self):
        extension = (self.pointA.displacement-self.pointB.displacement).length() - self.target
        return 0.5*self.forceConstant*extension**2

    def resolve(self):
        d = self.pointB.displacement - self.pointA.displacement
        length = d.length()
        if length != 0:
            factor = (length - self.target) / (length / self.forceConstant)
        else:
            factor = self.target * 0.5
        correction = factor * d
        self.pointA.correct(correction)
        self.pointB.correct(-correction)

    def draw(self):
        pygame.draw.aaline(screen.surface, self.colour, self.pointA.displacement, self.pointB.displacement, 1)

class Rod(Constraint):
    forceConstant = 0.4
    parent = None
    colour = (165, 165, 165)

    def __init__(self, pointA, pointB):
        Constraint.__init__(self, pointA, pointB)
        self.pivot = pointA.displacement + 0.5*(pointB.displacement - pointA.displacement)
        constraints.append(self)
    def resolve(self):
        Constraint.resolve(self)
        A = self.pointA.displacement
        B = self.pointB.displacement
        P = self.pivot

        L = B-A
        t = (P-A).dot(L)/L.dot(L)
        t = max(0, min(t, 1))
        D = A + L*t
        X = P - D
        X += L*(t-0.5)


        pygame.gfxdraw.filled_circle(screen.surface, int(P.x), int(P.y), 2, fixedPoint.colour)

        self.pointA.correct(X)
        self.pointB.correct(X)

    def draw(self):
        Constraint.draw(self)
        pygame.gfxdraw.filled_circle(screen.surface, int(self.pivot.x), int(self.pivot.y), 1, (0, 0, 0))


class rigidBody:
    def __init__(self, parts):
        # self.parts = parts
        for part in parts:
            part.parent = self


def createBox(x, y, width, height):
    x -= width / 2
    y -= height / 2
    tl = Point(x, y)
    tr = Point(x + width, y)
    bl = Point(x, y + height)
    br = Point(x + width, y + height)
    c1 = Constraint(tl, tr)
    c2 = Constraint(tr, br)
    c3 = Constraint(br, bl)
    c4 = Constraint(bl, tl)
    c5 = Constraint(tl, br)
    # c6 = Constraint(tr, bl)
    box = [tl, tr, bl, br, c1, c2, c3, c4, c5]
    return rigidBody(box)


def createCircle(x, y, r, s):
    circle = []
    centre = Point(x, y)
    pp = None
    angle = 0
    while angle < 2 * math.pi:
        xi = x + r * math.sin(angle)
        yi = y + r * math.cos(angle)
        p = Point(xi, yi)
        c = Constraint(centre, p)
        circle.append(c)
        if pp is not None:
            c2 = Constraint(p, pp)
            circle.append(c2)
        pp = p
        angle += 2 * math.pi / s
    c = Constraint(pp, circle[0].pointB)
    circle.append(c)

    return rigidBody(circle)


def createTruss(x, y, width, height):
    topAnchor = fixedPoint(x, y)
    bottomAnchor = fixedPoint(x, y + width)
    beam = Constraint(topAnchor, bottomAnchor)
    truss = [topAnchor, bottomAnchor, beam]
    for i in range(1, height + 1):
        newTop = Point(x + i * width, y)
        newBottom = Point(x + i * width, y + width)
        beam1 = Constraint(topAnchor, newTop)
        beam2 = Constraint(bottomAnchor, newBottom)
        beam3 = Constraint(newTop, bottomAnchor)
        beam4 = Constraint(newTop, newBottom)
        beam5 = Constraint(topAnchor, newBottom)
        topAnchor = newTop
        bottomAnchor = newBottom
        truss.extend([newTop, newBottom, beam1, beam2, beam3, beam4, beam5])
    return rigidBody(truss)


def createRope(startPoint, endPoint, res):
    rope = []
    length = endPoint.displacement- startPoint.displacement
    for i in range(res):
        if i != res - 1:
            nextPoint = Point(startPoint.displacement.x + (length.x / res),
                              startPoint.displacement.y + (length.y / res))
        else:
            nextPoint = endPoint
        c = Constraint(startPoint, nextPoint)
        startPoint = nextPoint
        rope.append(c)
    return rigidBody(rope)


def createNewtonsCradle(x, y, length, radius, angle, amount):
    angle = -math.radians(angle)
    anchor = fixedPoint(x, y)
    ball = Point(x + (length * math.sin(angle)), y + (length * math.cos(angle)))
    ball.radius = radius
    bar = Constraint(anchor, ball)
    cradle = rigidBody([anchor, ball, bar])
    x += radius * 2
    for i in range(amount):
        anchor = fixedPoint(x + (i * radius * 2), y)
        ball = Point(x + (i * radius * 2), y + length)
        ball.radius = radius
        bar = Constraint(anchor, ball)
        cradle = rigidBody([anchor, ball, bar])

def __main__():
    global bodies, points, constraints, G, screen, fps, pixelsPerMetre

    earth = Planet(5.972 * 10 ** 24, 6.371 * 10 ** 6, 40)
    #createTruss(30, 30, 40, 6)
    #rigidBody([Constraint(fixedPoint(10, screen.height - 30), fixedPoint(screen.width - 10, screen.height - 30))])
    #createNewtonsCradle(260, 200, 200, 20, 30, 4)
    #createRope(fixedPoint(300, 10), Point(300, 310), 100)
    #createCircle(300, 40, 30, 10)

    #p = Body(100 + 20, screen.height - 100 - 20, 1, 20)
    #q = Body(screen.width-100-20, screen.height - 100-20, 1, 20)
    rod = Rod(Point(100, screen.height - 100), Point(screen.width-100, screen.height - 100))
    p1 = None
    p2 = None
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = not running

            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if event.button == 1:
                    p1 = p2
                    if p1 != None:
                        connect = False
                        for point in points:
                            if (mouse - point.displacement).length() <= point.radius * 2:
                                p2 = point
                                connect = True
                        if not connect:
                            p2 = Point(mouse[0], mouse[1])
                        c = Constraint(p1, p2)
                    else:
                        p2 = fixedPoint(mouse[0], mouse[1])
                elif event.button == 3:
                    p1 = p2
                    p2 = fixedPoint(mouse[0], mouse[1])
                    if p1 != None:
                        c = Constraint(p1, p2)
                elif event.button == 2:
                    size = 2 * pixelsPerMetre * random.random() + 5
                    newBox = createBox(mouse[0], mouse[1], size, size)
                else:
                    size = 2 * pixelsPerMetre * random.random() + 5
                    newBody = Body(mouse[0], mouse[1], 1, size)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    bodies = [earth]
                    del points[:]
                    del constraints[:]
                    p1 = None
                    p2 = None
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    running = not running

        if not paused:
            steps = 2 ** 6  # Proportional to precision of simulation
            dt = 1 / steps
            screen.surface.fill((224, 247, 255))
            for step in range(steps):
                totalEnergy = 0
                screen.surface.fill((224, 247, 255))
                drawText('2D physics simulation utilising multi-step Verlet integration', 30, 2, 0)
                drawText(' V  0.12', 12, 2, 20)

                for constraint in constraints:
                    constraint.resolve()
                    constraint.draw()
                    totalEnergy += constraint.elasticPotentialEnergy()

                for body in bodies:
                    for other in bodies:
                        if body is other:
                            break
                        body.collide(other, dt)
                        gravity = body.gravitationalForce(other)
                        body.applyForce(-gravity)
                        other.applyForce(gravity)

                    for constraint in constraints:
                        if not constraint.parent == body:
                            body.constraintCollide(constraint, dt)

                    if not isinstance(body, Planet) and keepBodiesInScreen:
                        body.borderCollide(dt)
                    body.simulate(dt)
                    body.draw()
                    totalEnergy += body.energy()

                #print(totalEnergy, " J")
                #pygame.time.Clock().tick(fps)
                pygame.display.update()

__main__()
pygame.quit()
quit()
