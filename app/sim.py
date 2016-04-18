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
import math
import threading


class Canvas:
    def __init__(self, width, height, windowCaption):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(windowCaption)

    def drawText(self, text, fontSize, x, y):
        font = pygame.font.SysFont(None, fontSize)
        TextSurf = font.render(text, True, (224 / 4, 247 / 4, 255 / 4))
        TextRect = TextSurf.get_rect()
        TextRect.x = x;
        TextRect.y = y;
        self.surface.blit(TextSurf, TextRect)


class Body:
    anchored = False
    parent = None
    colour = (255, 165, 0)
    elasticity = 1

    def __init__(self, simulation, x, y, m=1, r=10):
        self.simulation = simulation
        self.simulation.bodies.append(self)
        self.displacement = pygame.math.Vector2(x, y)
        self.previousDisplacement = pygame.math.Vector2(x, y)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.radius = r
        self.mass = m

    def velocity(self):
        return self.displacement - self.previousDisplacement

    def kineticEnergy(self):
        return 0.5 * self.mass * self.velocity().length_squared()

    def gravitationalPotentialEnergy(self):
        GPE = 0
        for other in self.simulation.bodies:
            if self is other:
                break
            separation = (self.displacement - other.displacement).length()
            if separation > 0:
                GPE += self.simulation.G * self.mass * other.mass / (self.displacement - other.displacement).length()
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
        return self.simulation.G * self.mass * other.mass * separation.normalize() / separation.length_squared()

    def drag(self):
        v = self.velocity()
        if not v == pygame.math.Vector2(0, 0):
            p = self.density()
            A = math.pi * self.radius ** 2
            K = 0.47
            return -0.5*p*v.length_squared()*K*A*v.normalize()
        else:
            return v

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

        contactForce = self.mass*(separation.normalize() * lengthLimit - separation) / dt ** 2

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
        if self.displacement.x + self.radius > self.simulation.screen.width:
            normalForce.x -= (self.displacement.x + self.radius - self.simulation.screen.width) / dt ** 2
        if self.displacement.y < self.radius:
            normalForce.y += (self.radius - self.displacement.y) / dt ** 2
        if self.displacement.y + self.radius > self.simulation.screen.height:
            normalForce.y -= (self.displacement.y + self.radius - self.simulation.screen.height) / dt ** 2

        self.accelerate(normalForce)

    def draw(self):
        pygame.gfxdraw.filled_circle(self.simulation.screen.surface, int(self.displacement.x), int(self.displacement.y), int(self.radius), self.colour)
        pygame.gfxdraw.aacircle(self.simulation.screen.surface, int(self.displacement.x), int(self.displacement.y), int(self.radius),self.colour)

    def record(self):
        name = "Body"+str(self.simulation.bodies.index(self)+1)
        fields = [name,
                  self.displacement.length(),
                  self.velocity().length(),
                  self.acceleration.length(),
                  self.simulation.time]
        line = ",".join([str(field) for field in fields])
        self.simulation.recordCSV.write(line+'\n')

class Planet(Body):
    def __init__(self, simulation, m, r, colour=(0, 255, 0), h=10):
        Body.__init__(self, simulation, simulation.screen.width / 2, simulation.screen.height + r - h, m, r)
        self.colour = (0, 255, 0)
        self.h = h

    def draw(self):
        pygame.draw.rect(
            self.simulation.screen.surface,
            self.colour,
            (0, self.simulation.screen.height - self.h, self.simulation.screen.width, self.h))


class Point(Body):
    radius = 6

    def __init__(self, simulation, x, y, m=0.5):
        Body.__init__(self, simulation, x, y, m, 5)
        self.displacement = pygame.math.Vector2(x, y)
        self.previousDisplacement = pygame.math.Vector2(x, y)
        self.acceleration = pygame.math.Vector2(0, 0)
        simulation.points.append(self)

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


class Constraint:
    forceConstant = 0.4
    parent = None
    colour = (165, 165, 165)

    def __init__(self, simulation, pointA, pointB):
        self.simulation = simulation
        self.pointA = pointA
        self.pointB = pointB
        self.target = pointA.displacement.distance_to(self.pointB.displacement)
        self.simulation.constraints.append(self)

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
        pygame.draw.aaline(self.simulation.screen.surface,
                           self.colour,
                           self.pointA.displacement,
                           self.pointB.displacement, 1)


class Rod(Constraint):
    forceConstant = 0.4
    parent = None
    colour = (165, 165, 165)

    def __init__(self, simulation, pointA, pointB):
        Constraint.__init__(self, simulation, pointA, pointB)
        self.pivot = pointA.displacement + 0.5*(pointB.displacement - pointA.displacement)
        simulation.constraints.append(self)

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

        self.pointA.correct(X)
        self.pointB.correct(X)

    def draw(self):
        Constraint.draw(self)
        pygame.gfxdraw.filled_circle(self.simulation.screen.surface,
                                     int(self.pivot.x),
                                     int(self.pivot.y),
                                     1,
                                     fixedPoint.colour)


class rigidBody:
    def __init__(self, parts):
        # self.parts = parts
        for part in parts:
            part.parent = self


#earth = Planet(5.972 * 10 ** 24, 6.371 * 10 ** 6, 40)

class Simulation(threading.Thread):
    def __init__(self, G=6.674 * 10 ** (-11), airResistance=False, keepBodiesInScreen=True, allowUserInteraction=True,
                 steps=2**5, visual=True):

        threading.Thread.__init__(self)

        self.G = G
        self.airResistance = airResistance
        self.visual = visual
        self.steps = steps
        self.dt = 1 / self.steps
        self.time = 0

        if self.visual:
            self.keepBodiesInScreen = keepBodiesInScreen
            self.allowUserInteraction = allowUserInteraction
        else:
            self.keepBodiesInScreen = False
            self.allowUserInteraction = False

    def createBox(self, x, y, width, height):
        x -= width / 2
        y -= height / 2
        tl = Point(self, x, y)
        tr = Point(self, x + width, y)
        bl = Point(self, x, y + height)
        br = Point(self, x + width, y + height)
        c1 = Constraint(self, tl, tr)
        c2 = Constraint(self, tr, br)
        c3 = Constraint(self, br, bl)
        c4 = Constraint(self, bl, tl)
        c5 = Constraint(self, tl, br)
        # c6 = Constraint(self, tr, bl)
        box = [tl, tr, bl, br, c1, c2, c3, c4, c5]
        return rigidBody(box)

    def createCircle(self, x, y, r, s):
        circle = []
        centre = Point(x, y)
        pp = None
        angle = 0
        while angle < 2 * math.pi:
            xi = x + r * math.sin(angle)
            yi = y + r * math.cos(angle)
            p = Point(self, xi, yi)
            c = Constraint(self, centre, p)
            circle.append(c)
            if pp is not None:
                c2 = Constraint(self, p, pp)
                circle.append(c2)
            pp = p
            angle += 2 * math.pi / s
        c = Constraint(self, pp, circle[0].pointB)
        circle.append(c)
        return rigidBody(circle)

    def createTruss(self, x, y, width, height):
        topAnchor = fixedPoint(self, x, y)
        bottomAnchor = fixedPoint(self, x, y + width)
        beam = Constraint(self, topAnchor, bottomAnchor)
        truss = [topAnchor, bottomAnchor, beam]
        for i in range(1, height + 1):
            newTop = Point(self, x + i * width, y)
            newBottom = Point(self, x + i * width, y + width)
            beam1 = Constraint(self, topAnchor, newTop)
            beam2 = Constraint(self, bottomAnchor, newBottom)
            beam3 = Constraint(self, newTop, bottomAnchor)
            beam4 = Constraint(self, newTop, newBottom)
            beam5 = Constraint(self, topAnchor, newBottom)
            topAnchor = newTop
            bottomAnchor = newBottom
            truss.extend([newTop, newBottom, beam1, beam2, beam3, beam4, beam5])
        return rigidBody(truss)

    def createRope(self, startPoint, endPoint, res):
        rope = []
        length = endPoint.displacement - startPoint.displacement
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

    def createNewtonsCradle(self, x, y, length, radius, angle, amount):
        angle = -math.radians(angle)
        anchor = fixedPoint(self, x, y)
        ball = Point(self, x + (length * math.sin(angle)), y + (length * math.cos(angle)))
        ball.radius = radius
        bar = Constraint(self, anchor, ball)
        cradle = rigidBody([anchor, ball, bar])
        x += radius * 2
        for i in range(amount):
            anchor = fixedPoint(self, x + (i * radius * 2), y)
            ball = Point(self, x + (i * radius * 2), y + length)
            ball.radius = radius
            bar = Constraint(self, anchor, ball)
            cradle = rigidBody([anchor, ball, bar])

    def interact(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = not self.running

            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if event.button == 1:
                    p1 = p2
                    if p1 != None:
                        connect = False
                        for point in self.points:
                            if (mouse - point.displacement).length() <= point.radius * 2:
                                p2 = point
                                connect = True
                        if not connect:
                            p2 = Point(self, mouse[0], mouse[1])
                        c = Constraint(self, p1, p2)
                    else:
                        p2 = fixedPoint(self, mouse[0], mouse[1])
                elif event.button == 3:
                    p1 = p2
                    p2 = fixedPoint(self, mouse[0], mouse[1])
                    if p1 != None:
                        c = Constraint(self, p1, p2)
                elif event.button == 2:
                    size = 2 *50 * random.random() + 5
                    newBox = self.createBox(mouse[0], mouse[1], size, size)
                else:
                    size = 2 * 50 * random.random() + 5
                    newBody = Body(self, mouse[0], mouse[1], 1, size)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.bodies = [self.planet]
                    self.points = []
                    self.constraints = []
                    print('hdb')
                    p1 = None
                    p2 = None
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_ESCAPE:
                    self.running = not self.running

    def run(self):

        pygame.init()
        self.screen = Canvas(700, 500, "Newton's Laboratory - Simulation")
        self.fps = float("inf")
        self.bodies = []
        self.points = []
        self.constraints = []
        self.planet = Planet(self, 5.972 * 10 ** 24, 6.371 * 10 ** 6, 40)

        #self.createTruss(30, 30, 40, 6)
        #rigidBody([Constraint(fixedPoint(10, screen.height - 30), fixedPoint(screen.width - 10, screen.height - 30))])

        #self.createNewtonsCradle(260, 200, 200, 20, 30, 4)
        #createRope(fixedPoint(300, 10), Point(300, 310), 100)
        #createCircle(300, 40, 30, 10)

        #p = Body(100 + 20, screen.height - 100 - 20, 1, 20)
        #q = Body(screen.width-100-20, screen.height - 100-20, 1, 20)
        #rod = Rod(Point(100, screen.height - 100), Point(screen.width-100, screen.height - 100))

        Body(self,300, 30, 15, 20)
        p1 = None
        p2 = None
        self.running = True
        self.paused = False

        if not self.visual:
            pygame.display.iconify()

        basepath = ''
        if not __name__ == "__main__":
            basepath += 'data/'

        self.recordCSV = None
        i = 1
        while True:
            try:
                self.recordCSV = open(basepath+"simulation"+str(i)+".csv")
            except FileNotFoundError:
                break
            i += 1
        self.recordCSV = open(basepath+"simulation"+str(i)+".csv", 'w')
        self.recordCSV.write("Body ID, Displacement (m), Velocity (m/s), Acceleration (m/s\u00b2), Time (s)\n")

        while self.running:
            if self.allowUserInteraction:
                self.interact()

            if not self.paused:
                for step in range(self.steps):
                    totalEnergy = 0
                    self.screen.surface.fill((224, 247, 255))
                    self.screen.drawText('Visual 2D physics simulation utilising multi-step Verlet integration', 15, 2, 0)

                    for constraint in self.constraints:
                        constraint.resolve()
                        totalEnergy += constraint.elasticPotentialEnergy()
                        if self.visual:
                            constraint.draw()

                    for body in self.bodies:
                        body.record()
                        if self.airResistance:
                            body.applyForce(body.drag())

                        for other in self.bodies:
                            if body is other:
                                break
                            body.collide(other, self.dt)
                            gravity = body.gravitationalForce(other)
                            body.applyForce(-gravity)
                            other.applyForce(gravity)

                        for constraint in self.constraints:
                            if not constraint.parent == body:
                                body.constraintCollide(constraint, self.dt)

                        if not isinstance(body, Planet) and self.keepBodiesInScreen:
                            body.borderCollide(self.dt)
                        totalEnergy += body.energy()

                        if self.visual:
                            body.draw()
                        body.simulate(self.dt)
                    self.time += self.dt

                    #print(totalEnergy, " J")
                    #pygame.time.Clock().tick(self.fps)
                    pygame.display.update()
        self.recordCSV.close()
        pygame.quit()

if __name__ == "__main__":
    Simulation().start()
