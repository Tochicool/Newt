# import math
import pygame
from sympy import *
from sympy.vector import *

O = CoordSysCartesian( 'O' )

x, y, z, = O.base_vectors( )

t = symbols( 't', positive = True)

bodies = list( )
forces = list( )
w, h = 700, 500
pixelsPerMetre = 50
g = Rational(10 * pixelsPerMetre)
fps = 60
time = Rational( 0 )
tick = Rational( 1 / fps )
T = S.Infinity

pygame.init( )
init_printing( )


class Canvas:
    def __init__( self, width, height, windowcaption ):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode( (width, height) )
        pygame.display.set_caption( windowcaption )


screen = Canvas( w, h, 'Solver' )
simple_font = pygame.font.SysFont( "monospace", 15 )


class Body:
    c1, c2, c3 = Vector.zero, Vector.zero, Vector.zero

    s = (w / 2) * x + 0.5 * g * t ** 2 * y
    centre = s.subs( t, time ).dot( x ), s.subs( t, time ).dot( y )

    def __init__( self, name, mass, radius ):
        self.mass = mass
        self.r = radius
        self.name = name
        bodies.append( self )

    def set_nth_derivative( self, T, V, N ):
        n = 0
        while not self.s.diff( t, n + 1 ) == Vector.zero:
            n += 1

        S, C = symbols( 'S C' )

        S = diff( self.s, t, n ).subs( t, T )

        for i in range( n, -1, -1 ):
            # print('   Integrating gives...', S, ' + C')
            if i == N:
                C = (V - S).subs( t, T )
                # print('   ... C == ', C)
            else:
                C = (self.s.diff( t, i ) - S).subs( t, T )
                # print('   ... C == ', C)

            if i != 0:
                S = S.integrate( t ).doit( ) + C * t
                # print('   Therefore,  new S == ', S)
            else:
                S = S + C
                # print('   Therefore,  new S == ', S)

        # print(self.name, ' == ', S)
        self.s = S

    def set_displacement( self, k, T ):
        self.c3 = k - self.c1 * T ** 2 - self.c2 * T
        self.s = self.c1 * t ** 2 + self.c2 * t + self.c3

    def set_velocity( self, k, T ):
        c5 = k -  2 * self.c1 * T
        c6 = 2 * self.c1 * T ** 2 + self.c2 * T - k * T + self.c3
        self.c2 = c5
        self.c3 = c6
        self.s = self.c1 * t ** 2 + self.c2 * t + self.c3

    def set_acceleration( self, k, T ):
        c4 = Rational( 0.5 ) * k
        c5 = Rational( 2 ) * self.c1 * T + self.c2 - k * T
        c6 = Rational( 0.5 ) * k * T ** 2 - self.c1 * T ** 2 + self.c3
        self.c1 = c4
        self.c2 = c5
        self.c3 = c6
        self.s = self.c1 * t ** 2 + self.c2 * t + self.c3

    def get_next_collision_time_with( self, other ):

        next_collision_time = S.Infinity

        d = self.s - other.s
        sols = solve( Eq( d.magnitude( ), self.r + other.r ) )

        if isinstance( sols, bool ):
            return next_collision_time

        if len(sols) == 0:
            a = (self.c1-other.c1).magnitude()
            b = (self.c2-other.c2).magnitude()
            c = (self.c3-other.c3).magnitude() -self.r-other.r

            x = -b-sqrt(b**2-4*a*c)/(2*a)
            print(x)

        for sol in sols:
            if time < sol < next_collision_time:
                next_collision_time = sol

        return next_collision_time

    def draw( self ):
        self.centre = self.s.subs( t, time ).dot( x ), self.s.subs( t, time ).dot( y )

        pygame.draw.circle( screen.surface, (0, 0, 0), self.centre, self.r )

        label = simple_font.render( self.name, 1, (255, 255, 255) )
        screen.surface.blit( label, self.centre )


class Force:
    def __init__( self, body1, body2, time_of_contact ):
        self.body1 = body1
        self.body2 = body2
        self.time_of_contact = time_of_contact
        forces.append( self )


def update_sim( ):
    global T, forces
    T = S.Infinity
    forces = [ ]
    for body in bodies:
        for other in bodies:
            if body == other: break
            next_collision_time = body.get_next_collision_time_with( other )
            if time < next_collision_time < T:
                T = next_collision_time
                Force( body, other, T )
    print( 'T==', T )


def update_screen( ):
    screen.surface.fill( (255, 255, 255) )
    for body in bodies:
        body.draw( )
    pygame.display.update( )


p = Body( 'P', 10, 10 )
p.set_acceleration( g * x, time )
p.set_displacement( 100 * x + 300 * y, time )

q = Body( 'Q', 10, 50 )
q.set_acceleration( -g * x, time )
q.set_displacement( 600 * x + 300 * y, time )


def __main__( ):
    global t, time, forces

    update_sim( )

    running = True
    while running:
        if time + tick >= T:
            time = T

            for force in forces:
                if force.time_of_contact == T:
                    m1 = force.body1.mass
                    u1 = force.body1.s.diff( t ).subs( t, T )
                    m2 = force.body2.mass
                    u2 = force.body2.s.diff( t ).subs( t, T )

                    v2 = ((m1 * u1 + m1 * (u1 - u2) + m2 * u2) / (m1 + m2))
                    v1 = u2 + v2 - u1

                    # force.body1.set_nth_derivative( T, v1, 1 )
                    # force.body2.set_nth_derivative( T, v2, 1 )

                    force.body1.set_velocity( v1, T )
                    force.body2.set_velocity( v2, T )

            update_sim( )
        else:
            time += tick

        update_screen( )

        for event in pygame.event.get( ):
            if event.type == pygame.QUIT:
                running = not running


__main__( )
quit( )
