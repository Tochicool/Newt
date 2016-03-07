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

screen = canvas(700, 500, 'Verlet Test')
fps = 60

def drawText(text, fontSize, x, y):
    font = pygame.font.SysFont(None, fontSize)
    TextSurf = font.render(text, True, (224/4, 247/4, 255/4))
    TextRect = TextSurf.get_rect()
    TextRect.x = x; TextRect.y = y;
    screen.surface.blit(TextSurf, TextRect)

# GLOBAL VARIABLES
ppm = 50
g = pygame.math.Vector2(0, 9.81)
bodies = []
points = []
constraints = []

class Body:
    e = 1
    anchored = False
    parent = None
    def __init__(self, x, y, r):
        self.p = pygame.math.Vector2(x, y)
        self.pp = pygame.math.Vector2(x, y)
        self.a = pygame.math.Vector2(0, 0)
        self.r = r
        bodies.append(self)

    def simulate(self, delta):
        self.a *= delta**2
        p = (self.p*2)-self.pp+self.a

        self.pp = self.p
        self.p = p
        self.a *= 0

    def accelerate(self, vector):
        self.a += vector

    def borderCollide(self):
        if not self.r < self.p.x < screen.width-self.r:
            self.p.x = 2*self.pp.x-self.p.x-self.a.x
        if not self.r < self.p.y < screen.height-self.r:
            self.p.y = 2*self.pp.y-self.p.y-self.a.y
        self.p.x = max(self.p.x, self.r)
        self.p.x = min(self.p.x, screen.width-self.r)
        self.p.y = max(self.p.y, self.r)
        self.p.y = min(self.p.y, screen.height-self.r)

    def constraintCollide(self, constraint, preserveImpulse):
        Q = self.p # Centre of circle
        r = self.r+3+(self.p-self.pp).length() #Radius of circle
        P1 = constraint.point1.p # Start of line segment
        V = constraint.point2.p - P1 # Vector along the line

        a = V.dot(V)
        b = 2 * V.dot(P1 - Q)
        c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r**2
        disc = b**2 - 4 * a * c
        if disc < 0 or a == 0:
            return False, None
        else:
            sqrt_disc = math.sqrt(disc)
            t1 = (-b + sqrt_disc)/(2*a)
            t2 = (-b - sqrt_disc)/(2*a)

        if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
            return False, None

        t = max(0, min(1, -b/(2*a)))

        if (P1 + t*V - Q).length() <= r:
            i = P1 + t*V
        else:
            return False, None

        d = self.p - i

        length = d.length()
        target = r
        
        return True, i

    def collide(self, other, preserve_impulse):
        d = self.p - other.p

        length = d.length()
        target = self.r + other.r

        if length < target:
            v1 = self.p - self.pp
            v2 = other.p - other.pp
            if not length == 0:
                factor = 0.5*((length-target)/length)
            else:
                factor = target/2

            if not self.anchored:
                self.p -= d*factor
            if not other.anchored:
                other.p += d*factor

            damping = (self.e+other.e)/2

            if preserve_impulse and length != 0:
                f1 = (damping*(d*v1))/(length)**2
                f2 = (damping*(d*v2))/(length)**2

                v1 += f2*d - f1*d
                v2 += f1*d - f2*d

                self.pp = self.p - v1
                other.pp = other.p - v2

        

    def draw(self):
        if self.anchored:
            fill = (204, 0, 204)
        else:
            fill = (255, 165, 0)
        pygame.gfxdraw.filled_circle(screen.surface,int(self.p.x),int(self.p.y),int(self.r),fill)
        pygame.gfxdraw.aacircle(screen.surface,int(self.p.x),int(self.p.y),int(self.r),fill)

class Point(Body):
    r = 3
    def __init__(self, x, y):
        self.p = pygame.math.Vector2(x,y)
        self.pp = pygame.math.Vector2(x,y)
        self.a = pygame.math.Vector2(0,0)
        points.append(self)

    def correct(self, vector):
        self.p += vector

class fixedPoint(Point):
    anchored = True
    def accelerate(self, vector):
        pass
    def simulate(self, delta):
        pass
    def correct(self, vector):
        pass

class Constraint:
    forceConstant = 0.4
    parent = None
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.target = point1.p.distance_to(self.point2.p)
        constraints.append(self)

    def resolve(self):
        pos1 = self.point1.p
        pos2 = self.point2.p
        d = pos2-pos1
        length = d.length()
        if length != 0:
            factor = (length-self.target)/(length/self.forceConstant)
        else:
            factor = self.target*0.5
        correction = factor*d
        self.point1.correct(correction)
        self.point2.correct(-correction)

    def draw(self):
        fill = (165, 165, 165)
        pygame.draw.line(screen.surface, fill, self.point1.p, self.point2.p, 6)


class rigidBody:
    def __init__(self, parts):
        #self.parts = parts
        for part in parts:
            part.parent = self

def createBox(x, y, width, height):
    x -= width/2
    y -= height/2
    tl = Point(x, y)
    tr = Point(x+width, y)
    bl = Point(x, y+height)
    br = Point(x+width, y+height)
    c1 = Constraint(tl, tr)
    c2 = Constraint(tr, br)
    c3 = Constraint(br, bl)
    c4 = Constraint(bl, tl)
    c5 = Constraint(tl, br)
    #c6 = Constraint(tr, bl)
    box = [tl, tr, bl, br, c1, c2, c3, c4, c5]
    return rigidBody(box)

def createTruss(x, y, width, height):
    topAnchor = fixedPoint(x, y)
    bottomAnchor = fixedPoint(x, y+width)
    beam = Constraint(topAnchor, bottomAnchor)
    truss = [topAnchor, bottomAnchor, beam]
    for i in range(1, height+1):
        newTop = Point(x+i*width, y)
        newBottom = Point(x+i*width, y+width)
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
    length = endPoint.p - startPoint.p
    for i in range(res):
        if i != res-1:
            nextPoint = Point(startPoint.p.x+(length.x/res), startPoint.p.y+(length.y/res))
        else:
            nextPoint = endPoint

        c = Constraint(startPoint, nextPoint)
        startPoint = nextPoint
        rope.append(c)
    return rigidBody(rope)

def createNewtonsCradle(x, y, length, radius, angle, amount):
    angle = -math.radians(angle)
    anchor = fixedPoint(x, y)
    ball = Point(x +(length*math.sin(angle)), y+(length*math.cos(angle)))
    ball.r = radius
    c = Constraint(anchor, ball)
    cradle = rigidBody([anchor, ball, c])
    x+=radius*2
    for i in range(amount):
        anchor = fixedPoint(x+(i*radius*2), y)
        ball = Point(x+(i*radius*2), y+length)
        ball.r = radius
        c = Constraint(anchor, ball)
        cradle = rigidBody([anchor, ball, c])

def __main__():
    truss = createTruss(30, 30, 40, 6)
    #platform = rigidBody([Constraint(fixedPoint(10, screen.height-30), fixedPoint(screen.width-10, screen.height-30))])
    createNewtonsCradle(260, 200, 200, 20, 30, 4)
    #rope = createRope(fixedPoint(300, 10), Point(300, 310), 100)
    p1 = None
    p2 = None
    program = True
    while program:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program = False

            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if event.button == 1:
                    p1 = p2
                    if p1 != None:
                        connect = False
                        for point in points:
                            if (mouse - point.p).length() <= point.r*2:
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
                    size = 2*ppm*random.random()+5
                    #newBody = Body(mouse[0], mouse[1], size)
                    newBox = createBox(mouse[0], mouse[1], size, size)
                else:
                    size = 2*ppm*random.random()+5
                    newBody = Body(mouse[0], mouse[1], size)                    

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x: 
                    del bodies[:] 
                    del points[:]
                    del constraints[:]
                    p1 = None; p2 = None;

        steps = 15 # Proportional to precision of simulation
        delta = 1/steps
        totalE = 0
        screen.surface.fill((224, 247, 255))
        for step in range(steps):
            screen.surface.fill((224, 247, 255))
            drawText('2D physics simulation utilising multi-step verlet interation', 30, 2, 0)
            drawText(' V  0.12', 12, 2, 20)
            for body1 in bodies:
                body1.accelerate(g)
                body1.simulate(delta)
                for body2 in bodies:
                    if not body1 == body2:
                        body1.collide(body2, False)
                    else: break
                for other in constraints:
                    body1.constraintCollide(other, False)
                v = body1.p-body1.pp
                totalE+=((body1.r/2)*(v.length()**2) + (body1.r*g.y*(screen.height-body1.p.y-(body1.r/2))))
                body1.borderCollide()
                body1.draw()

            for constraint in constraints:
                constraint.resolve()
                constraint.draw()

            for point in points:
                point.draw()
                point.accelerate(g)
                point.simulate(delta)
                for other in constraints:
                    if point.parent != other.parent:
                        point.constraintCollide(other, False)
                    else: break
                for other in bodies:
                    if point.parent != other.parent:
                        point.collide(other, True)
                    else: break
                for other in points:
                    if point.parent != other.parent:
                        point.collide(other, True)
                    else: break
                point.borderCollide()
                v = point.p-point.pp
                totalE+=((point.r/2)*(v.length()**2) + (point.r*g.y*(screen.height-point.p.y-(point.r/2))))
            pygame.time.Clock().tick(fps)
            pygame.display.update()
        #print(totalE/1000, ' KJ')
__main__()
pygame.quit()
quit()


